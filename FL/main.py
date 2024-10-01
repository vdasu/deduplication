import torch
import numpy as np
import random
import math
from torch.optim import AdamW
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.utils.data import DataLoader, random_split
from ep_mpd import MultiPartyDeduplicator, EgPsiType, EgPsiDataType
import os
import time

from config import *
from utils import TextDataset, train_client, compute_test_perplexity, get_text_dataset
from copy import deepcopy

os.environ["HF_HOME"] = CACHE_PATH

# set all seeds
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)


device = "cpu"
if torch.cuda.is_available():
    device = "cuda"


tokenizer = GPT2Tokenizer.from_pretrained(
    MODEL_NAME, bos_token=BOS_TOKEN, eos_token=EOS_TOKEN, pad_token=PAD_TOKEN
)

model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
model.resize_token_embeddings(len(tokenizer))
model = model.to(device)

if not os.path.exists(MODEL_PATH):
    os.mkdir(MODEL_PATH)

if not os.path.exists(MODEL_CACHE):
    os.mkdir(MODEL_CACHE)

torch.save(
    model.state_dict(),
    os.path.join(MODEL_CACHE, f"global_{DATASET}.pt"),
)


############ Load dataset ############

full_data = get_text_dataset(dataset_name=DATASET)

train_data, test_data = random_split(full_data, [1 - TEST_RATIO, TEST_RATIO])

test_set = TextDataset(data=test_data, tokenizer=tokenizer)

############ Implant duplicates in dataset ############

if DUPLICATE_RATE > 0:
    train_data_len = len(train_data)
    num_duplicates = int(DUPLICATE_RATE * train_data_len)
    duplicate_indices = np.random.choice(train_data_len, num_duplicates, replace=True)
    train_data = torch.utils.data.ConcatDataset(
        [
            train_data,
            torch.utils.data.Subset(train_data, duplicate_indices),
        ]
    )

############ Split dataset among clients ############

splits = [1 / CLIENTS] * CLIENTS
if sum(splits) != 1:
    splits[-1] += 1 - sum(splits)
client_data = random_split(train_data, splits)

client_data_list = []

for data in client_data:
    client_data_list.append(list(data))



############ EP-MPD Deduplication of datasets ############

if USE_EPMPD:
    
    if TYPE == 1:
        eg_type = EgPsiType.TYPE1
    elif TYPE == 2:
        eg_type = EgPsiType.TYPE2
    else:
        raise Exception("Unknown EG PSI type")

    # First step is local deduplication by each client
    for i in range(CLIENTS):
        client_data_list[i] = list(set(client_data_list[i]))
    
    # Next clients use EP-MPD
    mpd = MultiPartyDeduplicator(client_data=client_data_list, data_type=EgPsiDataType.STR, eg_type=eg_type, debug=False)
    mpd.deduplicate()

    # Client datasets are now deduplicated
    for i in range(CLIENTS):
        client_data_list[i] = mpd.get_client_dataset(i)
    

client_datasets = [ 
    TextDataset(data=client_data_list[i], tokenizer=tokenizer) 
    for i in range(CLIENTS)
]

client_data_loaders = [
    DataLoader(client_datasets[i], batch_size=BATCH_SIZE, shuffle=True)
    for i in range(CLIENTS)
]

############ FedAvg FL TRAINING STARTS ############

best_model = None
best_loss = math.inf
best_round = -1

for round in range(ROUNDS):

    avg_loss = 0

    # Train the clients
    for client in range(CLIENTS):
        client_state = torch.load(os.path.join(MODEL_CACHE, f"global_{DATASET}.pt"))
        client_model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
        client_model.resize_token_embeddings(len(tokenizer))

        client_model.load_state_dict(client_state)

        start = time.time()
        client_loss = train_client(
            client_model,
            client_data_loaders[client],
            client,
            round,
        )
        torch.cuda.synchronize()
        end = time.time()
        print(f"Client {client} round {round} took {end - start} seconds\n")
        avg_loss += client_loss

        new_client_state = {
            "model": client_model.state_dict(),
        }

        torch.save(
            new_client_state,
            os.path.join(MODEL_CACHE, f"client_{client}_{DATASET}.pt"),
        )

    avg_loss /= CLIENTS

    print("\n\nAverage loss after round {} is {}\n".format(round, avg_loss))
    print("Average loss after round {} is {}\n".format(round, avg_loss))

    # Aggregate all client models and average them to get the new global model
    model_state_dict = deepcopy(model.state_dict())

    start = time.time()
    for i in range(CLIENTS):
        client_state_dict = torch.load(
            os.path.join(MODEL_CACHE, f"client_{i}_{DATASET}.pt")
        )["model"]
        for k in model_state_dict.keys():
            if i == 0:
                model_state_dict[k] = client_state_dict[k]
            else:
                model_state_dict[k] += client_state_dict[k]
            if i == CLIENTS - 1:
                model_state_dict[k] = torch.div(model_state_dict[k], CLIENTS)
    end = time.time()
    print(f"Aggregation took {end - start} seconds in round {round} \n")

    model.load_state_dict(model_state_dict)
    torch.save(
        model_state_dict,
        os.path.join(MODEL_CACHE, f"global_{DATASET}.pt"),
    )

    if avg_loss < best_loss:
        best_loss = avg_loss
        best_model = deepcopy(model.state_dict())
        best_round = round

############ Evaluate on test dataset ############

model.load_state_dict(best_model)

model.to(device)
model.eval()

prompt = BOS_TOKEN

generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
generated = generated.to(device)

# get ouputs using beam search
sample_outputs = model.generate(
    generated,
    max_new_tokens=50,
    num_beams=5,
    no_repeat_ngram_size=2,
    early_stopping=True,
    num_return_sequences=5,
)

for i, sample_output in enumerate(sample_outputs):
    print(
        "{}: {}\n\n".format(
            i, tokenizer.decode(sample_output, skip_special_tokens=True)
        )
    )

torch.save(
    model.state_dict(),
    os.path.join(
        MODEL_PATH,
        f"{MODEL_NAME}_{DATASET}_{EPOCHS}epochs_{LEARNING_RATE}lr_{best_round}round_{SEED}_final.pt",
    ),
)

test_loader = DataLoader(test_set, batch_size=1, shuffle=True)

ppl = compute_test_perplexity(model, test_loader)

print(f"Test Perplexity: {ppl}")
