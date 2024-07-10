from typing import List
from ep_mpd.eg_psi.type1.client import ClientType1
from ep_mpd.eg_psi.type2.client import ClientType2
from ep_mpd.eg_psi.utils import keygen_pairwise_type1
from ep_mpd.eg_psi.type1.tp import SemiTrustedThirdPartyType1
from ep_mpd.eg_psi.type2.tp import SemiTrustedThirdPartyType2
from ep_mpd.eg_psi.utils import EgPsiType, EgPsiDataType
import time
from collections import defaultdict
from datetime import datetime


class MultiPartyDeduplicator:

    def __init__(self, client_data: List, data_type: EgPsiDataType, eg_type: EgPsiType = EgPsiType.TYPE1,
                 debug: bool = False):
        self.eg_type = eg_type
        self.data_type = data_type
        self.client_data = client_data  # List of all client's datasets
        self.clients = {}  # stores all clients. key is client id
        self.client_ids = []  # stores client ids
        if eg_type == EgPsiType.TYPE1:
            self.tp = SemiTrustedThirdPartyType1()
        elif eg_type == EgPsiType.TYPE2:
            self.tp = SemiTrustedThirdPartyType2()
        self.num_clients = 0
        self.debug = debug

        self.type1_encryptions = defaultdict(list)  # format: (level, (group0 time, group1 time))
        self.type1_receive_tp = defaultdict(list)  # format: (level, (group0 time, group1 time))
        self.type1_send_tp = defaultdict(list)  # format: (level, group0 send time)
        self.type1_receive_group_0 = defaultdict(list)  # format: (level, group0 receive time)

        self.type2_init_client = defaultdict(int)
        self.type2_init_tp = defaultdict(int)

        self.type2_send_group1 = defaultdict(lambda: defaultdict(list))
        self.type2_receive_group0 = defaultdict(lambda: defaultdict(list))
        self.type2_deduplicate_group0 = defaultdict(list)

        self.time_start = None
        self.time_end = None

        self.time_start = datetime.now()

        self.init_clients()

    def init_clients(self):

        self.num_clients = len(self.client_data)

        # Create all keys
        for client_id in range(self.num_clients):
            self.client_ids.append(client_id)

        if self.eg_type == EgPsiType.TYPE1:
            keys = keygen_pairwise_type1(client_ids=self.client_ids)

        # Create all clients
        for client_id, data in zip(self.client_ids, self.client_data):
            if self.eg_type == EgPsiType.TYPE1:
                client = ClientType1(client_id=client_id, data_type=self.data_type)
                client.set_keys(keys=keys[client_id])
            elif self.eg_type == EgPsiType.TYPE2:
                client = ClientType2(client_id=client_id, data_type=self.data_type)
            client.create_set(data_set=data)
            # if type2, then also encrypt all the data
            if self.eg_type == EgPsiType.TYPE2:
                start = time.perf_counter()
                tp_time = client.encrypt_elements(self.tp)
                end = time.perf_counter()

                self.type2_init_tp[client_id] = tp_time
                self.type2_init_client[client_id] = (end - start) - tp_time

            self.clients[client_id] = client

    def eg_psi_type1(self, left, mid, right, level):

        # TODO: We don't need every client to exchange with each other. If we assume all clients in Group 1 have higher client ID that group 0 then only group 1 needs to send to group 0 because group 0 clients are the ones who remove duplicates.

        if self.debug:
            print("\n\nGroup 0 IDs: ", self.client_ids[left:mid])
            print("Group 1 IDs: ", self.client_ids[mid:right])
            print("Level: ", level)

        group_0_encryptions = []
        group_1_encryptions = []
        group_0_receive_tp = []
        group_1_receive_tp = []
        group_0_receive = []
        group_0_send_tp = []

        # Create group 1 and send to TTP
        for client_id in self.client_ids[mid:right]:
            client = self.clients[client_id]
            client.set_group(1)

            start = time.perf_counter()
            client.encrypt_elements(other_client_ids=self.client_ids[left:mid])
            end = time.perf_counter()
            group_1_encryptions.append((client_id, end - start))

            start = time.perf_counter()
            self.tp.receive_from_client(client_group=1, client_id=client_id, client_data=client.s_prime)
            end = time.perf_counter()
            group_1_receive_tp.append((client_id, end - start))
            client.reset_client()

            if self.debug:
                print("Before -> Group 1, Client Id: {}, Client Data: {}".format(client_id, client.s))

        # Create group 0 and send to TTP
        for client_id in self.client_ids[left:mid]:
            client = self.clients[client_id]
            client.set_group(0)

            start = time.perf_counter()
            client.encrypt_elements(other_client_ids=self.client_ids[mid:right])
            end = time.perf_counter()
            group_0_encryptions.append((client_id, end - start))

            start = time.perf_counter()
            self.tp.receive_from_client(client_group=0, client_id=client_id, client_data=client.s_prime)
            end = time.perf_counter()
            group_0_receive_tp.append((client_id, end - start))

            if self.debug:
                print("Before -> Group 0, Client Id: {}, Client Data: {}".format(client_id, client.s))

            start = time.perf_counter()
            r = self.tp.send_to_client(client_group=0, client_id=client_id, client_data=client.s_prime)
            end = time.perf_counter()
            group_0_send_tp.append((client_id, end - start))

            start = time.perf_counter()
            client.set_intersection(r)
            end = time.perf_counter()
            group_0_receive.append((client_id, end - start))

            if self.debug:
                print("After -> Group 0, Client Id: {}, Client Data: {}".format(client_id, client.s))

        # Clients in group 1 only reset and do no compute intersection
        for client_id in self.client_ids[mid:right]:
            # r = self.tp.send_to_client(client_group=1, client_id=client_id)
            client = self.clients[client_id]
            # client.set_intersection(r)
            client.reset_client()
            if self.debug:
                print("After -> Group 1, Client Id: {}, Client Data: {}".format(client_id, client.s))

        self.type1_encryptions[level].append((group_0_encryptions, group_1_encryptions))
        self.type1_receive_tp[level].append((group_0_receive_tp, group_1_receive_tp))
        self.type1_send_tp[level].append(group_0_send_tp)
        self.type1_receive_group_0[level].append(group_0_receive)

        # Clean up for next round. Clients automatically clean up after intersection
        self.tp.clear_all()

    def eg_psi_type2(self, left, mid, right, level):

        # TODO: We don't need every client to exchange with each other. If we assume all clients in Group 1 have higher client ID that group 0 then only group 1 needs to send to group 0 because group 0 clients are the ones who remove duplicates.

        if self.debug:
            print("\n\nGroup 0 IDs: ", self.client_ids[left:mid])
            print("Group 1 IDs: ", self.client_ids[mid:right])
            print("Level: ", level)

        for client_id in self.client_ids[left:mid]:
            client = self.clients[client_id]
            client.set_group(0)

        for client_id in self.client_ids[mid:right]:
            client = self.clients[client_id]
            client.set_group(1)

        # clients from group 1 send their elements to clients in group 0
        for client_id_0 in self.client_ids[left:mid]:
            for client_id_1 in self.client_ids[mid:right]:
                client_0 = self.clients[client_id_0]
                client_1 = self.clients[client_id_1]

                start = time.perf_counter()
                id_1, s_prime_1 = client_1.send_to_client()
                end = time.perf_counter()
                self.type2_send_group1[level][client_id_1].append(end - start)

                start = time.perf_counter()
                client_0.receive_from_client(client_id=id_1, s_prime=s_prime_1)
                end = time.perf_counter()
                self.type2_receive_group0[level][client_id_0].append(end - start)

        # Group 0 clients update their datasets after removing duplicates
        for client_id in self.client_ids[left:mid]:

            start = time.perf_counter()
            self.clients[client_id].set_intersection()
            end = time.perf_counter()

            self.type2_deduplicate_group0[level].append((client_id, end - start))

            if self.debug:
                print("After -> Group 0, Client Id: {}, Client Data: {}".format(client_id, self.clients[client_id].s))

        # Group 1 clients reset only since only Group 0 clients remove their duplicates
        for client_id in self.client_ids[mid:right]:
            self.clients[client_id].reset_client()

            if self.debug:
                print("After -> Group 1, Client Id: {}, Client Data: {}".format(client_id, self.clients[client_id].s))

        # TP resets. Clients reset automatically after they remove duplicates
        # self.tp.reset_secret()

    def deduplicate(self):

        # Recurse down the tree and run eg_psi on groups
        def mpd(left, right, level):
            # base case, trivially intersection free
            if right == left + 1:
                return
            mid = (left + right) // 2
            if self.debug:
                print("Level: ", level)
                print("Indices Left: ", self.client_ids[left:mid])
                print("Indices Right: ", self.client_ids[mid:right])
                print()
            mpd(left, mid, level + 1)
            mpd(mid, right, level + 1)
            if self.eg_type == EgPsiType.TYPE1:
                self.eg_psi_type1(left, mid, right, level)
            elif self.eg_type == EgPsiType.TYPE2:
                self.eg_psi_type2(left, mid, right, level)

        mpd(0, self.num_clients, 0)
        self.time_end = datetime.now()

    def get_combined_dataset(self) -> List[int | str]:

        combined_dataset = []

        for client_id in self.clients:
            combined_dataset += self.clients[client_id].get_deduplicated_dataset()

        return combined_dataset

    def get_client_dataset(self, client_id: int) -> List[int | str]:
        return self.clients[client_id].get_deduplicated_dataset()

    def print_timing_stats(self):

        if self.eg_type == EgPsiType.TYPE1:
            total_time = 0
            levels = list(self.type1_encryptions.keys())
            levels.sort()

            for level in levels[::-1]:
                print("\nCurrent Level: ", level)
                print("\nClient Encryptions and TP Receive\n")
                client_encryptions = self.type1_encryptions[level]
                tp_receive = self.type1_receive_tp[level]
                tp_send = self.type1_send_tp[level]
                client_dedup = self.type1_receive_group_0[level]

                level_time = 0
                encrypt_receive_time = 0
                for ((group_0_encryptions, group_1_encryptions), (group_0_receive, group_1_receive)) in zip(
                        client_encryptions, tp_receive):

                    print("\nGroup 0 clients")
                    for data_encrypt, data_receive in zip(group_0_encryptions, group_0_receive):
                        assert data_receive[0] == data_encrypt[0]
                        print(
                            "\nClient: {}, Client Encrypt Time: {}".format(data_encrypt[0], round(data_encrypt[1], 5)))
                        print("Client: {}, TP Receive Time: {}".format(data_receive[0], round(data_receive[1], 5)))
                        encrypt_receive_time = max(data_receive[1] + data_encrypt[1], encrypt_receive_time)

                    print("\nGroup 1 clients")
                    for data_encrypt, data_receive in zip(group_1_encryptions, group_1_receive):
                        assert data_receive[0] == data_encrypt[0]
                        print(
                            "\nClient: {}, Client Encrypt Time: {}".format(data_encrypt[0], round(data_encrypt[1], 5)))
                        print("Client: {}, TP Receive Time: {}".format(data_receive[0], round(data_receive[1], 5)))
                        encrypt_receive_time = max(data_receive[1] + data_encrypt[1], encrypt_receive_time)

                level_time += encrypt_receive_time
                print("\nClient Deduplicate and TP Send\n")

                tp_accum_time = 0
                effective_client_times = []
                for (group_0_send_tp, group_0_receive_tp) in zip(tp_send, client_dedup):

                    for data_send, data_receive in zip(group_0_send_tp, group_0_receive_tp):
                        assert data_send[0] == data_receive[0]
                        print("\nClient: {}, TP Send Time: {}".format(data_send[0], round(data_send[1], 5)))
                        print("Client: {}, Client Deduplicate Time: {}".format(data_receive[0],
                                                                               round(data_receive[1], 5)))
                        effective_client_times.append(tp_accum_time + data_send[1] + data_receive[1])
                        tp_accum_time += data_send[1]

                send_deduplicate_time = max(effective_client_times)
                level_time += send_deduplicate_time
                print("\nLevel: {}, Time for entire level: {}".format(level, round(level_time, 5)))
                total_time += level_time

            print("\n\nTotal time for entire protocol: {}".format(round(total_time, 5)))

            print("\nWall clock time\nStart time: ", self.time_start)
            print("End time: ", self.time_end)
        else:
            total_time = 0
            levels = list(self.type2_send_group1.keys())
            levels.sort()

            for client_id in self.type2_init_client:
                total_time += self.type2_init_client[client_id]
                total_time += self.type2_init_tp[client_id]

            print("\nSetup time: {}".format(round(total_time, 5)))

            for client_id in self.type2_init_client:
                print("\nClient: {}, Client Setup Time: {}".format(client_id, self.type2_init_client[client_id]))

            for client_id in self.type2_init_client:
                print("\nClient: {}, TP Setup Time: {}".format(client_id, self.type2_init_tp[client_id]))

            for level in levels[::-1]:
                print("\n\nCurrent Level: ", level)
                level_time = 0

                send_time = 0
                receive_time = 0

                send_group1 = self.type2_send_group1[level]
                receive_group0 = self.type2_receive_group0[level]

                for client_id in send_group1:
                    send_time = max(send_time, max(send_group1[client_id]))
                    print("\nClient: {}".format(client_id))
                    print("Send Times: ", [round(i, 5) for i in send_group1[client_id]])
                    print("\nClient: {}, Client Send Time: {}".format(client_id, max(send_group1[client_id])))

                for client_id in receive_group0:
                    receive_time = max(receive_time, max(receive_group0[client_id]))
                    print("\nClient: {}".format(client_id))
                    print("Receive Times: ", [round(i, 5) for i in receive_group0[client_id]])
                    print("\nClient: {}, Client Receive Time: {}".format(client_id, max(receive_group0[client_id])))

                print("\nSend Time of Group 1: {}".format(round(send_time, 5)))
                print("\nReceive Time of Group 0: {}".format(round(receive_time, 5)))
                level_time += send_time + receive_time

                deduplicate_group0 = self.type2_deduplicate_group0[level]
                deduplicate_time = 0

                for (client_id, client_dedup_time) in deduplicate_group0:
                    deduplicate_time = max(client_dedup_time, deduplicate_time)
                    print("\nClient: {}, Client Deduplicate Time: {}".format(client_id, round(client_dedup_time, 5)))

                level_time += deduplicate_time

                total_time += level_time

            print("\n\nTotal time for entire protocol: {}".format(round(total_time, 5)))

            print("\nWall clock time\nStart time: ", self.time_start)
            print("End time: ", self.time_end)
