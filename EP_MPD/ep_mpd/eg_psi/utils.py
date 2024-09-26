from typing import List, Dict
import struct
import base64
import os
import math
from collections import defaultdict
from enum import Enum, auto

from ep_mpd.eg_psi.type1.prp_key import PRPKey


class EgPsiType(Enum):
    TYPE1 = auto()
    TYPE2 = auto()


class EgPsiDataType(Enum):
    INT = auto()
    STR = auto()


def keygen_pairwise_type1(client_ids: List[int]) -> Dict[int, PRPKey]:
    keys = defaultdict(list)

    for i in range(len(client_ids) - 1):
        for j in range(i + 1, len(client_ids)):
            key = PRPKey(key=os.urandom(32), iv=os.urandom(16))
            keys[client_ids[i]].append((client_ids[j], key))
            keys[client_ids[j]].append((client_ids[i], key))

    return keys


def encode_element(ele: int | str) -> bytes:
    if type(ele) is int:
        ele_bytes = struct.pack("<I", ele)
    elif type(ele) is str:
        ele_bytes = str.encode(ele)
    return ele_bytes


def decode_element(ele_bytes: bytes, data_type: EgPsiDataType) -> int | str:
    if data_type == EgPsiDataType.INT:
        ele = struct.unpack("<I", ele_bytes)[0]
    elif data_type == EgPsiDataType.STR:
        ele = base64.b64encode(ele_bytes.decode())
    return ele

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
