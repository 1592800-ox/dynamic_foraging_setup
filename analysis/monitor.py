import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# TODO test if the Axes object are the same as the ones initialized by
def monitor_train(left_p, right_p, trial_indices, choices, rewarded, ax: plt.Axes):
    # choose left and get rewarded, 0 for left in choices
    left_rewarded = np.where((not choices) and (rewarded))[0]
    left_unrewarded = np.where((not choices) and (not rewarded))[0]
    right_rewarded = np.where((choices) and (rewarded))[0]
    right_unrewarded = np.where((choices) and (not rewarded))[0]

    