# Federated Learning and Deduplication

This folder contains code to analyze the effect of duplicated data in federated learning and use the EP-MPD protocol to securely deduplicate the training datasets held by clients before the federated learning training procedure.

## Installation Instructions

1. Create the environment using anaconda: `conda env create -f environment.yml`
2. Activate the environment: `conda activate fed_dedup`
3. Install the EP-MPD library: `cd ../EP_MPD && pip install .`
4. Download the datasets from [here](https://drive.google.com/drive/folders/1SYycnxYaLr4iPeMGxGhtxX1Zs8P_UKLI?usp=drive_link) and place them in the `datasets` folder.

## Usage

The FL experiments use `config.py` script to the set the training parameters. The `config.py` script is documented with comments next to each parameter. Most of the parameters (learning rate, batch size, model, etc.) are self explanatory and the various options are described in the `config.py` file. We explain some of the important parameters here.

1. `DUPLICATE_RATE`: The duplicate rate sets the percentage of duplicates among the datasets held by the clients. For example, a `DUPLICATE_RATE = 0.3` means that 30% of the data samples held by all clients is repeated more than once.
2. `CLIENTS`: Sets the number of clients for FL training. The chosen dataset is equally divided among the number of clients.
3. `ROUNDS`: Number of FL training rounds to perform in the FedAvg algorithm.
4. `EPOCHS`: Number of epochs of local training a client performs in each training round.
5. `TEST_RATIO`: Ratio of samples in the dataset to hold out for evaluating the perplexity of the trained models. For example, a `TEST_RATIO = 0.2` means that 20% of the data samples in the original dataset are held out for the test data.
6. `USE_EPMPD`: Whether to perform EP-MPD deduplication or not. Setting this to True will override the effects of `DUPLICATE_RATE` as it performs deduplication among the clients before training. If you want to analyze the effects of duplicates in training data on running time and perplexity, always set this to False. 
7. `TYPE`: Type of EP-MPD to use. Can be 1 or 2.

Once the `config.py` folder has configured with the desired parameters, simply run `main.py`. 

## Reproducing the Paper's Results

The logs folder contains all the logs of our experiments along with the associated `config.py` files. These logs can be used to generate Table 1 and Table 2 in the paper. Run `print_stats.py` to generate the data for the tables. To reproduce the results on your own machine, simply use the provided `config.py` files and then run `main.py`.

_Warning: The FL experiments in the paper require a GPU with at least 50GB memory like the RTX A6000 and can take up to 2 days to run._
