import numpy as np

data = np.load("data/processed/windowed_data.npy", allow_pickle=True)

print("Total signal groups:", len(data))

for i in range(min(2, len(data))):
    print("\nSignal key:", data[i]["key"])
    print("First window:", data[i]["X"][0])
    print("First target:", data[i]["y"][0])
