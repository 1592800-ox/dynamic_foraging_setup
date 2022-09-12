# real-time plotting of mice's behaviour during the session
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def monitor_train(left_p, axes: plt.Axes, trial_indices, choices, rewarded):
    axes.clear()
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
        axes.plot([left_rewarded], -1.1, marker='o', color='c')
    if left_unrewarded.size > 0:
        axes.plot([left_unrewarded], -1.2, marker='x', color='m')
    if right_rewarded.size > 0:
        axes.plot([right_rewarded], 1.1, marker='o', color='c')
    if right_unrewarded.size > 0:
        axes.plot([right_unrewarded], 1.2, marker='x', color='m')

    nan_indices = np.where(choices == -1)
    left_indices = np.where(choices == 0)
    print(choices)
    choices[left_indices] = -1
    choices[nan_indices] = 0
    print(choices)

    if choices.size > 5:  
        choices = np.convolve(choices, np.ones(5), 'same') / 5
        sns.lineplot(x=trial_indices, y=choices, ax=axes, color='black')
    
    set_prob = []

    for p in left_p:
        if p > 0.5:
            set_prob.append(-p)
        else:
            set_prob.append(1-p)
    
    sns.lineplot(x=trial_indices, y = set_prob, color='blue', ax=axes)
    axes.set_title('trial index: %d, reward given: %d' % (trial_indices[-1], np.sum(rewarded == 1)))
