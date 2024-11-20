# Efficient Privacy-Preserving Multi-Party Deduplication (EP-MPD)

This library implements the Efficient Privacy-Preserving Multi-Party Deduplication (EP-MPD) protocol for removing all pairwise duplicates among datasets held by 2 or more clients in federated learning.

## Installation

The package requires a `python=3.10` environment. We recommend creating a new environment using `conda` to prevent any potential issues with your existing environments.

1. (Optional but recommended) `conda create -n ep_mpd python=3.10`
2. (Optional but recommended) `conda activate ep_mpd`
3. `git clone https://github.com/vdasu/deduplication.git`
4. `cd EP_MPD`
5. `pip install .`


## Usage

The following components from the `ep_mpd` library are required to run deduplication for a set of clients:

1. `EgPsiType`: Enum that is either `EgPsiType.TYPE1` or `EgPsiType.TYPE2` for Type 1 and Type 2 EG-PSI's respectively. Type 1 is based on symmetric key cryptography and Type 2 is based on public key cryptography. Refer to the paper for a detailed description of each type. In the paper, `EgPsiType.TYPE1` and `EgPsiType.TYPE2` are referred to as EG-PSI<sup>(I)</sup> and EG-PSI<sup>(II)</sup> respectively.
2. `EgPsiDataType`: Enum that is either `EgPsiDataType.INT` or `EgPsiDataType.STR` for integer and string datatypes respectively. Currently, the library works with integer and string datatypes only.
3. `MultiPartyDeduplicator`: Class that provides the privacy-preserving deduplication functionality. The `MultiPartyDeduplicator` has the following attributes:
   1. `client_data`: A 2-D list where each row is a client's dataset. For example, a 2-D list of shape `m*n` contains the data of `m` clients where the dataset size is `n`. The protocol assumes that each client performs local deduplication to remove any duplicates that exist within their own datasets prior to multi-party deduplication.
   2. `data_type`: The datatype of the datasets i.e. `EgPsiDataType.INT` or `EgPsiDataType.STR`.
   3. `eg_type`: The type of EG-PSI to use for deduplication. Either `EgPsiType.TYPE1` or `EgPsiType.TYPE2`.
  
   The class provides the following functions:
   1. `deduplicate()`: Runs the EP-MPD protocol with the provided attributes.
   2. `get_client_dataset(client_id: int)`: Returns the deduplicated dataset for client with ID=`client_id`. The `client_id` is 0 indexed, and it refers to the dataset in the 2-D `client_data` list.
   3. `get_combined_dataset()`: Returns the union of all clients' datasets after deduplication.
   4. `print_timing_stats()`: Provides detailed running time information of the EP-MPD protocol execution.

The annotated code snippet below provides a simple example with 3 clients with a dataset size of 5 elements:

```python
# Imports
from ep_mpd import MultiPartyDeduplicator, EgPsiType, EgPsiDataType

# Create three clients' datasets
client1_data_original = [1,2,3,4]
client2_data_original = [3,4,5,6]
client3_data_original = [1,5,7,8]

all_client_data = [client1_data_original, client2_data_original, client3_data_original]

# Create the deduplicator class with EG-PSI Type 1. Pass EgPsiType.TYPE2 to eg_type for Type 2 instead.
mpd = MultiPartyDeduplicator(client_data=all_client_data, data_type=EgPsiDataType.INT, eg_type=EgPsiType.TYPE1)

# Run EP-MPD
mpd.deduplicate()

# Get each client's dataset after deduplication
client1_data_dedup = mpd.get_client_dataset(0)
client2_data_dedup = mpd.get_client_dataset(1)
client3_data_dedup = mpd.get_client_dataset(2)

print("Client 1 deduplicated dataset: ", client1_data_dedup) # [2]
print("Client 2 deduplicated dataset: ", client2_data_dedup) # [3,4,6]
print("Client 3 deduplicated dataset: ", client3_data_dedup) # [1,5,7,8]

# Compare with naive Python set 

# Get union of all client's datasets after EP-MPD deduplication
dedup_data_all = mpd.get_combined_dataset()
dedup_data_all.sort()

# Get union of all client's datasets after naive Python set
from operator import add
from functools import reduce

original_data_all = reduce(add, all_client_data)
original_data_all = list(set(original_data_all))
original_data_all.sort()

for x, y in zip(dedup_data_all, original_data_all):
    assert x == y
```

## Reproduce the paper's results

This repository provides all the original log files and python scripts to re-run the paper's experiments or generate the plots in the paper. The `run_paper` folder contains the logs for all the EP-MPD benchmarking experiments. The python scripts in the `run_paper` folder can be used to generate the plots in Figure 6, 7, and 8 in the paper. You would need a local TeX installation and `matplotlib` (`pip install matplotlib`). The `run_paper` folder also contains the specifications of the machine used to run the experiments in the paper in `platform_spec.txt`. 

The scripts and folders under `run_paper` are:

1. `type1_runs` and `type2_runs`: These folders contain the detailed execution of the EP-MPD protocol using the parameters mentioned in the paper for EG-PSI Type-1 and Type-2 respectively. The parameter for each run can be parsed from the name of the log file. For example, `10_50_0.3.log` contains the log for 50 clients, with 2^10 dataset size, and 30% duplication.
2. `plot_epmpd.py`: Used to generate Figures 6a, 7a, and 8a. This shows the effect of client count, dataset size, and duplication percentage on EP-MPD running time.
3. `plot_client.py`: Used to generate Figures 6b, 7b, and 8b. This shows the effect of client count, dataset size, and duplication percentage on client running time.
4. `plot_tee.py`: Used to generate Figures 6c, 7c, and 8c. This shows the effect of client count, dataset size, and duplication percentage on TEE running time.
5. `run.sh`: The bash script runs the deduplication protocol using the parameters from the paper. Note that the paper considers a large scale setting and it may not be feasible to run them on commodity hardware. Refer to the next section for smaller scale experiments.
6. `Figures`: Contains the plots used in the paper.

To run the scripts, use the following commands:

```bash
cd run_paper
chmod +x run.sh
./run.sh
```

## Small Scale Experiments

The `run_small_scale` folder provides scripts to run experiments on commodity hardware on a smaller scale. The folder contains the same files as the `run_paper` folder but with smaller parameters. We test with client count in [5,10,15,20,25] and dataset size in [2^5, 2^7, 2^10, 2^13, 2^15]. These experiments run in under 15 minutes on an M1 Pro Macbook Pro. The `type1_runs` and `type2_runs` folders contain the logs for the small-scale experiments. These will be overwritten after running `run.sh`. Like before, the `plot*.py` scripts are used to generate the corresponding plots. 

To run the scripts, use the following commands:

```bash
cd run_small_scale
chmod +x run.sh
./run.sh
```

## Custom Parameters

To validate the paper's claims with a different set of parameters, `main_int.py` can be used. The script takes the following command line arguments:

```
usage: main_int.py [-h] [--psi-type PSI_TYPE] [--num-clients NUM_CLIENTS] [--num-ele NUM_ELE]
                   [--seed SEED] [--dup-per DUP_PER]

Runs the EP-MPD deduplication protocol

options:
  -h, --help            show this help message and exit
  --psi-type PSI_TYPE   EG-PSI Type (1 or 2). Default is 1.
  --num-clients NUM_CLIENTS
                        Number of clients (Integer). Default is 10.
  --num-ele NUM_ELE     Number of elements in each client's dataset (Integer). Default is 10.
  --seed SEED           Random seed for dataset creation (Integer). Default is 42.
  --dup-per DUP_PER     Percentage of duplicates (Between 0.0 and 1.0). Default is 0.3.
```

For example, to get the timing results for 40 clients with 2^19 datasize and 30% duplicates you need to run:

```
python main_int.py --psi-type 1 --num-clients 40 --num-ele 524288 --dup-per 0.3
```

Since we simulate all clients on a single machine, depending on the resources available, you might run into out of memory issues. We recommend starting with 10 clients and 2^10 elements before gradually increasing the number of clients and dataset size.

## String Data

The `main_str.py` script contains a simple example for string data with hardcoded lists for 8 clients. Simply run `python main_str.py`.
