# functions used to evaluated an animal's performance in a session

import numpy as np
import matplotlib.pyplot as plt

def get_nan_percent(choices: np.ndarray):
    nan_percent = []
    for i in np.arange(5, len(choices), step=1):
        nan_count = 0
        for j in np.arange(i-5, i, step=1):
            if choices[j] == -1:
                nan_count += 1
        nan_percent.append(float(nan_count) / 5.0)
    return nan_percent


def get_performance(choices: np.ndarray, leftP: np.ndarray, version: str):
    if len(choices) != len(leftP) or not len(choices > 0):
        try:
            raise RuntimeError
        finally:
            print('choices and set probability has different lengths')
    if '10' in version:
        return float(sum(choices != -1)) / float(len(choices))
    chose_right = np.array(choices == 1, dtype=bool) 
    right_adv = np.array(leftP < 0.5, dtype=bool)
    adv = np.logical_and(chose_right, right_adv)
    return float(sum(adv)) / float(len(choices))


def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)


def plot_nan_percent(nan_percents: np.ndarray):
    y, error = tolerant_mean(nan_percents)
    error = error / 2
    lower = y - error
    upper = y + error
    x = np.arange(5, len(y) + 5)

    # Draw plot with error band and extra formatting to match seaborn style
    fig, ax = plt.subplots(figsize=(9,5))
    ax.plot(x, y, label='signal mean')
    ax.plot(x, lower, color='tab:blue', alpha=0.1)
    ax.plot(x, upper, color='tab:blue', alpha=0.1)
    ax.fill_between(x, lower, upper, alpha=0.2)
    ax.set_xlabel('timepoint')
    ax.set_ylabel('signal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.show()