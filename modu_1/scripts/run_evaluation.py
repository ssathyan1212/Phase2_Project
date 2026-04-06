import numpy as np
from evaluation.visualization import plot_signal
# Example signals
actual = np.random.rand(100)
predicted = actual + np.random.normal(0, 0.05, 100)

plot_signal(actual, predicted)
