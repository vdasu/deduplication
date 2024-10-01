# ML PARAMETERS
MODEL_NAME = "gpt2-medium"
BATCH_SIZE = 4
LEARNING_RATE = 5e-5
DUPLICATE_RATE = 0.0 # between 0 and 1
MAX_SEQ_LEN = 1000
EPOCHS = 10
DATASET = "Poetry"
# DATASET = "IMDB"

EOS_TOKEN = "<|endoftext|>"
BOS_TOKEN = "<|startoftext|>"
PAD_TOKEN = "<|pad|>"

TEST_RATIO = 0.2
SEED = 123

# EP-MPD PARAMETERS
# If True, then the EP-MPD deduplication will be applied to client datasets before FL training.
# This will result in 0% duplication and will override the effects of DUPLICATE_RATE.
# Setting this to true will effectively result in DUPLICATE_RATE = 0.0
USE_EPMPD = True
TYPE = 1 # Type can be 1 or 2

# OTHER PARAMETERS
MODEL_PATH = "trained_models"
MODEL_CACHE = "models_cache"

# FL PARAMETERS
CLIENTS = 10
ROUNDS = 5


# Other params
CACHE_PATH = "/scratch/vad5173"
