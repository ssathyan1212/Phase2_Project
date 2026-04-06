# preprocessing/read_algorithm.py
from collections import defaultdict
def read_extract(can_rows):
    """
    Groups CAN data by CAN ID and signal
    Equivalent to READ signal extraction
    """
    extracted = defaultdict(list)
    for row in can_rows:
        key = (row["can_id"], row["signal"])
        extracted[key].append(float(row["value"]))
    return extracted
