# ML PARAMETERS
MODEL_NAME = "gpt2-medium" # gpt2, gpt2-medium, gpt2-large, gpt2-xl
BATCH_SIZE = 8
LEARNING_RATE = 5e-5
DUPLICATE_RATE = 0.0 # between 0 and 1. 0 means no duplicates. 
EPOCHS = 5
DATASET = "Jokes" # Jokes, IMDB, Rotten, Haiku, WikiBio, Shakespeare, Sonnets, Poetry

EOS_TOKEN = "<|endoftext|>"
BOS_TOKEN = "<|startoftext|>"
PAD_TOKEN = "<|pad|>"

TEST_RATIO = 0.2 # Ratio of test samples
SEED = 123 # Random seed for reproducibility

# Directories to save models
MODEL_PATH = "trained_models"
MODEL_CACHE = "models_cache"

# FL PARAMETERS
CLIENTS = 10
ROUNDS = 5

# Path to download and cache huggingface models and data
CACHE_PATH = "./"
