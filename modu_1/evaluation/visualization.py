# evaluation/visualization.py

import matplotlib.pyplot as plt

def plot_signal(actual, predicted):
    plt.plot(actual, label="Actual")
    plt.plot(predicted, label="Predicted")
    plt.legend()
    plt.show()
