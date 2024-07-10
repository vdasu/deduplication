from ep_mpd.mpd import MultiPartyDeduplicator
from ep_mpd.eg_psi.utils import EgPsiType, EgPsiDataType
from create_elements import create_int_elements, create_int_elements_pairwise
import random
import argparse

parser = argparse.ArgumentParser(description="Runs deduplication protocol")
parser.add_argument('--psi-type', type=int, help="EG-PSI Type (1 or 2)", default=1)
parser.add_argument('--num-clients', type=int, help="Number of clients", default=10)
parser.add_argument('--num-ele', type=int, help="Number of elements", default=10)
parser.add_argument('--seed', type=int, help="Random seed", default=42)
parser.add_argument('--dup-per', type=float, help="Percentage of duplicates", default=0.3)

args = parser.parse_args()

eg_psi_type = EgPsiType.TYPE1 if args.psi_type == 1 else EgPsiType.TYPE2
num_elements = args.num_ele
num_clients = args.num_clients
dup_per = args.dup_per

random.seed(args.seed)

client_data = []


client_data_dict = create_int_elements_pairwise(num_clients, num_elements, dup_per)

for i in client_data_dict:
    client_data.append(client_data_dict[i])

non_duplicated_list = []

for data in client_data:
    non_duplicated_list.extend(data)


mpd = MultiPartyDeduplicator(client_data=client_data, data_type=EgPsiDataType.INT, eg_type=eg_psi_type, debug=False)
mpd.deduplicate()
mpd_full_dataset = mpd.get_combined_dataset()

client_data_full = []
for data in client_data:
    client_data_full += data
client_data_full = list(set(client_data_full))
client_data_full.sort()

mpd_full_dataset.sort()

for x, y in zip(client_data_full, mpd_full_dataset):
    assert x == y

print("EG PSI Type: ", eg_psi_type)

mpd.print_timing_stats()

print("\nTotal data with duplicates: ", len(non_duplicated_list))
print("Total data without duplicates: ", len(mpd_full_dataset))
