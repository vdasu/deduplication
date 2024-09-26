from ep_mpd import MultiPartyDeduplicator, EgPsiType, EgPsiDataType


client1 = [
    "Unique 1.",
    "This is sentence 1.",
    "This is sentence 3.",
    "This is sentence 5.",
    "This is sentence 8."
]

client2 = [
    "Unique 2.",
    "This is sentence 2.",
    "This is sentence 7.",
    "This is sentence 3.",
    "This is sentence 6."
]

client3 = [
    "Unique 3.",
    "This is sentence 3.",
    "This is sentence 2.",
    "This is sentence 4.",
    "This is sentence 1."
]

client4 = [
    "Unique 4.",
    "This is sentence 4.",
    "This is sentence 6.",
    "This is sentence 8.",
    "This is sentence 5."
]

client5 = [
    "Unique 5.",
    "This is sentence 5.",
    "This is sentence 1.",
    "This is sentence 6.",
    "This is sentence 2."
]

client6 = [
    "Unique 6.",
    "This is sentence 6.",
    "This is sentence 3.",
    "This is sentence 5.",
    "This is sentence 2."
]

client7 = [
    "Unique 7.",
    "This is sentence 7.",
    "This is sentence 3.",
    "This is sentence 1.",
    "This is sentence 4."
]

client8 = [
    "Unique 8.",
    "This is sentence 8.",
    "This is sentence 5.",
    "This is sentence 2.",
    "This is sentence 6."
]

client_data = [client1, client2, client3, client4, client5, client6, client7, client8]

print("Datasets before deduplication")
for client_id, data in enumerate(client_data):
    print("Client ID: {}, Data: {}".format(client_id, data))

mpd = MultiPartyDeduplicator(client_data=client_data, data_type=EgPsiDataType.STR, eg_type=EgPsiType.TYPE2, debug=False)
mpd.deduplicate()
mpd_full_dataset = mpd.get_combined_dataset()

print("\n\nDatasets after deduplication")
for client_id in mpd.clients:
    print("Client ID: {}, Data: {}".format(client_id, mpd.get_client_dataset(client_id=client_id)))


print("\n\nNaive deduplication using Python set")
client_data_full = []
for data in client_data:
    client_data_full += data
client_data_full = list(set(client_data_full))
client_data_full.sort()
print(client_data_full)

print("\nFull dataset after MPD")
mpd_full_dataset.sort()
print(mpd_full_dataset)

for x, y in zip(client_data_full, mpd_full_dataset):
    assert x == y

print("\nEP-MPD deduplication is same as Python naive deduplication")
