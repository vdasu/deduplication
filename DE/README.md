# Duplication Eliminator

Implements dataset deduplication in federated learning using multiparty private set intersection

## Usage

Create a Python environment with `python=3.10` and install the dependencies in `requirements.txt`.

The deduplication library supports string and int formats. To replicate the results in the paper, run `main_full_int.py`

Sample usage: `python3 main_full_int.py --psi-type 2 --num-ele 4096 --num-clients 5 --dup-per 0.3`

Above command runs DE with EG-PSI Type 2 with 5 clients, 4096 set size, and 30% duplication.

For example with string data, refer `main_full_str.py`. This script hard codes a few strings to test deduplication with string data.
