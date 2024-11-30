# FL and ML PARAMETERS
MODEL_NAME = "gpt2-medium"
BATCH_SIZE = 8
LEARNING_RATE = 5e-5
DUPLICATE_RATE = 0.0 # between 0 and 1
MAX_SEQ_LEN = 500
EPOCHS = 5
CLIENTS = 10
ROUNDS = 5
DATASET = "IMDB"
EOS_TOKEN = "<|endoftext|>"
BOS_TOKEN = "<|startoftext|>"
PAD_TOKEN = "<|pad|>"
TEST_RATIO = 0.2 # Ratio of samples to use in the Test dataset for final perplexity evaluation
SEED = 123 # Random seed to distribute dataset among clients, create duplicates, and create the test dataset

# EP-MPD PARAMETERS
# If True, then the EP-MPD deduplication will be applied to client datasets before FL training.
# This will result in 0% duplication and will override the effects of DUPLICATE_RATE.
# Setting this to true will effectively result in DUPLICATE_RATE = 0.0
USE_EPMPD = True
TYPE = 1 # Type can be 1 or 2

# Other params
CACHE_PATH = "/scratch/vad5173"
MODEL_PATH = "trained_models"
MODEL_CACHE = "models_cache"
