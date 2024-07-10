import math
from collections import defaultdict


def create_int_elements(num_clients, num_ele, dup_per):
    unique_ele_cnt = math.floor((1 - dup_per) * num_ele)
    repeat_ele_cnt = math.ceil(dup_per * num_ele)

    client_data = defaultdict(list)

    for i in range(num_clients):
        client_data[i].extend(range(i * unique_ele_cnt, (i + 1) * unique_ele_cnt))

    repeat_ele = range((num_clients + 2) * unique_ele_cnt, (num_clients + 2) * unique_ele_cnt + repeat_ele_cnt)

    for i in range(num_clients):
        client_data[i].extend(repeat_ele)

    return client_data


def create_int_elements_pairwise(num_clients, num_ele, dup_per):
    unique_ele_cnt = math.floor((1 - dup_per) * num_ele)
    repeat_ele_cnt = math.ceil(dup_per * num_ele)

    client_data = defaultdict(list)

    for i in range(num_clients):
        client_data[i].extend(range(i * unique_ele_cnt, (i + 1) * unique_ele_cnt))

    left = num_clients * unique_ele_cnt
    rep_cnt_per_client = math.ceil(repeat_ele_cnt / (num_clients - 1))

    for i in range(num_clients - 1):
        for j in range(i + 1, num_clients):
            right = left + rep_cnt_per_client
            data = range(left, right)
            client_data[i].extend(data)
            client_data[j].extend(data)
            left = right + 1

    return client_data
