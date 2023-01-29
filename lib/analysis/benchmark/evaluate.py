# functions used to evaluated an animal's performance in a session

import enum
from re import L
from turtle import st
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
    if '21' in version:
        leftP = leftP[:400]
        choices = choices[:400]
    else:
        leftP = leftP[:450]
        choices = choices[:450]
    chose_right = np.array(choices == 1, dtype=bool) 
    right_adv = np.array(leftP < 0.5, dtype=bool)
    adv_right = np.logical_and(chose_right, right_adv)
    chose_left = np.array(choices == 0, dtype=bool) 
    left_adv = np.array(leftP > 0.5, dtype=bool)
    adv_left = np.logical_and(chose_left, left_adv)
    adv_percent = float(sum(adv_right) + sum(adv_left)) / float(len(choices))
    switches = get_switches(leftP) / 10.0
    return adv_percent + switches

def get_performance_new(choices: np.ndarray, leftP: np.ndarray, mode: str):
    if len(choices) != len(leftP) or not len(choices > 0):
        try:
            raise RuntimeError
        finally:
            print('choices and set probability has different lengths')
    if 'motor' in mode:
        return float(sum(choices != -1)) / float(len(choices))
    if 'training_1' in mode:
        print('training_1 performance')
        leftP = leftP[:400]
        choices = choices[:400]
    else:
        print('training_2 performance')
        leftP = leftP[:450]
        choices = choices[:450]
    chose_right = np.array(choices == 1, dtype=bool) 
    right_adv = np.array(leftP < 0.5, dtype=bool)
    adv_right = np.logical_and(chose_right, right_adv)
    chose_left = np.array(choices == 0, dtype=bool) 
    left_adv = np.array(leftP > 0.5, dtype=bool)
    adv_left = np.logical_and(chose_left, left_adv)
    adv_percent = float(sum(adv_right) + sum(adv_left)) / float(len(choices))
    switches = get_switches(leftP) / 10.0
    return adv_percent + switches


def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    lens_sorted = np.sort(lens)
    lens_cutoff = int(np.percentile(lens_sorted, 90))
    # cut off trials indices that are not reached by 90% the sessions
    for ind, l in enumerate(arrs):
        if len(l) > lens_cutoff:
            arrs[ind] = l[:lens_cutoff]
    arr = np.ma.empty((np.max(lens_cutoff),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)


def plot_nan_percent(nan_percents: np.ndarray, title: str):
    y, error = tolerant_mean(nan_percents)
    error = error / 2
    lower = y - error
    upper = y + error
    x = np.arange(5, len(y) + 5)

    # Draw plot with error band and extra formatting to match seaborn style
    plt.tight_layout()
    plt.rcParams.update({'font.size': 18})
    fig, ax = plt.subplots(figsize=(5,5))
    x_axis = np.arange(start=0, stop=len(x), step=100)
    ax.plot(x, y, label='performance mean')
    ax.plot(x, lower, color='tab:blue', alpha=0.1)
    ax.plot(x, upper, color='tab:blue', alpha=0.1)
    ax.fill_between(x, lower, upper, alpha=0.2)
    ax.set_xlabel('trial index')
    ax.set_ylabel('nan percentage')
    ax.set_xticks(x_axis)
    # TODO set x axis accuracy
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title)
    plt.savefig(title + '.png', dpi=300, bbox_inches = "tight")
    plt.show()

def get_switches(leftP):
    switches = 0

    for index, p in enumerate(leftP):
        if index > 0 and p != leftP[index - 1]:
            switches += 1
    
    return switches