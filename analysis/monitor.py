from turtle import color
from matplotlib import markers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# TODO test if the Axes object are the same as the ones initialized by plt.subplots
def monitor_train(left_p, right_p, trial_indices, choices, rewarded, fig, ax: plt.Axes):
    # choose left and get rewarded, 0 for left in choices, -1 for nan trials
    left_rewarded = np.where((not choices) and (rewarded))[0]
    left_unrewarded = np.where((not choices) and (not rewarded))[0]
    right_rewarded = np.where((choices) and (rewarded))[0]
    right_unrewarded = np.where((choices) and (not rewarded))[0]

    if left_rewarded.size != 0:
        ax[0].plot([left_rewarded], 1.1, marker='o', color='c')
    if left_unrewarded.size != 0:
        ax[0].plot([left_unrewarded], 1.2, marker='x', color='m')
    if right_rewarded.size != 0:
        ax[1].plot([right_rewarded], 1.1, marker='o', color='c')
    if right_unrewarded.size != 0:
        ax[1].plot([right_unrewarded], 1.2, marker='x', color='m')

    choices_left = (choices==0).astype(int)
    choices_right = (choices==1).astype(int)
    if choices_left.size != 0:
        choices_left = np.convolve(choices_left, np.ones(5), 'same') / 5
        sns.lineplot(x=trial_indices, y=choices_left, ax=ax[0], c='black')
    if choices_right.size != 0:
        choices_right = np.convolve(choices_right, np.ones(5), 'same') / 5
        sns.lineplot(x=trial_indices, y=choices_right, ax=ax[1], c='black')

    plt.show(block=False)
    return ax
    