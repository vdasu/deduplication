from ep_mpd import MultiPartyDeduplicator, EgPsiType, EgPsiDataType, create_int_elements_pairwise
import random
import argparse

parser = argparse.ArgumentParser(description="Runs the EP-MPD deduplication protocol")
parser.add_argument('--psi-type', type=int, help="EG-PSI Type (1 or 2)", default=1)
parser.add_argument('--num-clients', type=int, help="Number of clients (Integer)", default=10)
parser.add_argument('--num-ele', type=int, help="Number of elements in each client's dataset (Integer)", default=10)
parser.add_argument('--seed', type=int, help="Random seed for dataset creation (Integer)", default=42)
parser.add_argument('--dup-per', type=float, help="Percentage of duplicates (0.0, 1.0)", default=0.3)
parser.add_argument('--debug', type=bool, help="Print detailed execution of protocol (True or False)", default=False)

args = parser.parse_args()

eg_psi_type = EgPsiType.TYPE1 if args.psi_type == 1 else EgPsiType.TYPE2
num_elements = args.num_ele
num_clients = args.num_clients
dup_per = args.dup_per
debug = args.debug

random.seed(args.seed)

client_data = []

client_data_dict = create_int_elements_pairwise(num_clients, num_elements, dup_per)

for i in client_data_dict:
    client_data.append(client_data_dict[i])

non_duplicated_list = []

for data in client_data:
    non_duplicated_list.extend(data)

mpd = MultiPartyDeduplicator(client_data=client_data, data_type=EgPsiDataType.INT, eg_type=eg_psi_type, debug=debug)
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
