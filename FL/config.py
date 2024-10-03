# LLM to use for training. Any Huggingface CausalLM model can be loaded here but we only test with GPT-2 Medium and Large.
MODEL_NAME = "gpt2-medium" # "gpt2-large"
# Batch size for training
BATCH_SIZE = 8
# Learnig rate for AdamW optimizer
LEARNING_RATE = 5e-5
# Percentage of duplicated samples among all clients dataset
DUPLICATE_RATE = 0.3 # between 0.0 and 1.0
# Max. sequence length for input data
MAX_SEQ_LEN = 500
# Number of epochs of local training
EPOCHS = 5
# No: of clients in FL training
CLIENTS = 10
# No: of rounds of FL training
ROUNDS = 5
# Special end of sentence, beginning of sentence, and pad tokens. This depends on the chosen Huggingface model. Below are the tokens for GPT-2 models.
EOS_TOKEN = "<|endoftext|>"
BOS_TOKEN = "<|startoftext|>"
PAD_TOKEN = "<|pad|>"

# Dataset to use for FL training
DATASET = "Haiku" # Jokes, Rotten, IMDB, Shakespeare, Sonnets, Poetry
# Ratio of samples to use in the Test dataset for final perplexity evaluation
TEST_RATIO = 0.2
# Random seed to distribute dataset among clients, create duplicates, and create the test dataset
SEED = 123

# EP-MPD PARAMETERS
# If True, then the EP-MPD deduplication will be applied to client datasets before FL training.
# This will result in 0% duplication and will override the effects of DUPLICATE_RATE.
# Setting this to true will effectively result in DUPLICATE_RATE = 0.0
USE_EPMPD = True
TYPE = 1 # Type can be 1 or 2

# Other params
# Path for Huggingface cache
CACHE_PATH = "/scratch/vad5173"
MODEL_PATH = "trained_models"
MODEL_CACHE = "models_cache"