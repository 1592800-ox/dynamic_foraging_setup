# real-time plotting of mice's behaviour during the session
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def monitor_train(left_p, right_p, axes: plt.Axes, trial_indices, choices, rewarded):
    axes[0].clear()
    axes[1].clear()
    choices = np.array(choices)
    rewarded = np.array(rewarded)

    # merge two plots into one, left is -1, shows leftP accurately
    left_rewarded = np.array([])
    left_unrewarded = np.array([])
    right_rewarded = np.array([])
    right_unrewarded = np.array([])
    # choose left and get rewarded, 0 for left in choices, -1 for nan trials
    if (choices == 0).size > 0:
        if (rewarded == 1).size > 0:
            left_rewarded = np.where((choices == 0) & (rewarded == 1))[0]
        if (rewarded == 1).size > 0:
            left_unrewarded = np.where((choices == 0) & (rewarded == 0))[0]
    if (choices == 1).size > 0:
        if (rewarded == 1).size > 0:
            right_rewarded = np.where((choices == 1) & (rewarded == 1))[0]
        if (rewarded == 1).size > 0:
            right_unrewarded = np.where((choices == 1) & (rewarded == 0))[0]

    if left_rewarded.size > 0:
        axes[0].plot([left_rewarded], 1.1, marker='o', color='c')
    if left_unrewarded.size > 0:
        axes[0].plot([left_unrewarded], 1.2, marker='x', color='m')
    if right_rewarded.size > 0:
        axes[1].plot([right_rewarded], 1.1, marker='o', color='c')
    if right_unrewarded.size > 0:
        axes[1].plot([right_unrewarded], 1.2, marker='x', color='m')

    print(rewarded)
    print(choices)
    choices_left = choices == 0
    choices_right = choices == 1
    choices_left.astype(int)
    choices_right.astype(int)
    print(choices_left)
    print(choices_right)
    print(trial_indices) 
    if choices.size > 5:  
        if choices_left.size > 0:
            choices_left = np.convolve(choices_left, np.ones(5), 'same') / 5
            print(choices_left)
            sns.lineplot(x=trial_indices, y=choices_left, ax=axes[0], color='black')
        if choices_right.size > 0:
            choices_right = np.convolve(choices_right, np.ones(5), 'same') / 5
            print(choices_right)
            sns.lineplot(x=trial_indices, y=choices_right, ax=axes[1], color='black')

    sns.lineplot(x=trial_indices, y = left_p, color='blue', ax=axes[0])
    sns.lineplot(x=trial_indices, y = right_p, color='blue', ax=axes[1])