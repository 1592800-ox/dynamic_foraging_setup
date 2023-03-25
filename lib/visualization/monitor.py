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
    if (choices == -1).size > 0:
        nan_trials = np.where((choices == -1))[0]

    # nan_indices = np.where(choices == -1)
    # left_indices = np.where(choices == 0)
    # choices[left_indices] = -1
    # choices[nan_indices] = 0
    
    set_prob = []

    for p in left_p:
        if p > 0.5:
            set_prob.append(-p)
        else:
            set_prob.append(1-p)
    
    sns.lineplot(x=trial_indices, y = set_prob, color='blue', ax=axes)
    axes.set_title('trial index: %d, reward given: %d' % (trial_indices[-1], np.sum(rewarded == 1)))
    if right_rewarded.size > 0:
        sns.scatterplot(x=right_rewarded, y=1.1, marker='|', color='royalblue', ax=axes, s=100)
    if left_rewarded.size > 0:
        sns.scatterplot(x=left_rewarded, y=-1.1, marker='|', color='royalblue', ax=axes, s=100, label='rewarded')
    if right_unrewarded.size > 0:
        sns.scatterplot(x=right_unrewarded, y=1.2, marker='|', color='deeppink', ax=axes, s=100, label='no_reward')
    if left_unrewarded.size > 0:
        sns.scatterplot(x=left_unrewarded, y=-1.2, marker='|', color='deeppink', ax=axes, s=100)
    if nan_trials.size > 0:
        sns.scatterplot(x=nan_trials, y=-1.15, marker='|', color='black', ax=axes, s=100, label='nan_trials')
        sns.scatterplot(x=nan_trials, y=1.15, marker='|', color='black', ax=axes, s=100)

    if choices.size > 5:
        responses = np.convolve(choices, np.ones(5)/5, mode='same')
        sns.lineplot(x=trial_indices, y=responses.reshape(1, -1)[0], ax=axes, label='choices')
    sns.lineplot(x=trial_indices, y=set_prob, ax=axes, label='reward')

    # sns.scatterplot(x=left_choices, y=1.1, marker='o', color='deeppink', ax=axes[1], s=10, label='left_choices')
    # sns.scatterplot(x=nan_trials, y=1.1, marker='o', color='black', ax=axes[1], s=10, label='nan_trials')
    # sns.scatterplot(x=right_choices, y=1.1, marker='o', color='royalblue', ax=axes[1], s=10, label='right_choices')

    axes.legend(bbox_to_anchor=(1.15, 0.7))

