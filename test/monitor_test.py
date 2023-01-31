from secrets import choice
import numpy as np
import matplotlib.pyplot as plt

from lib.visualization.monitor import monitor_train

trial_indices = np.arange(0, 60, dtype=int)
leftP_test = [0.1] * 20 + [0.8]*20 + [0.15]*20
choice_test = [1] * 23 + [-1] + [0] * 36 
rewards = [1] * 10 + [0] * 13 + [-1] + [1] * 10 + [0] * 26
fig, axes = plt.subplots(1, 1)

monitor_train(left_p=leftP_test, axes=axes, trial_indices=trial_indices, choices=choice_test, rewarded=rewards)

plt.show(block=True)