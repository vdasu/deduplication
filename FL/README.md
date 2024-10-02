# Federated Learning and Deduplication

_Note: The FL experiments require a GPU with at least 50GB memory like the RTX A6000 and can take up to 2 days to run._

This folder contains code to analyze the effect of duplicated data in federated learning and use the EP-MPD protocol to securely deduplicate the training datasets held by clients before the federated learning training procedure.

## Installation Instructions

1. Create the environment using anaconda: `conda env create -f environment.yml`
2. Activate the environment: `conda activate fed_dedup`
3. Install the EP-MPD library: `cd ../EP_MPD && pip install .`

## Usage



