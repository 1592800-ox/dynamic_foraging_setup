# functions used to evaluated an animal's performance in a session

import numpy as np

def get_nan_percent(choices: np.ndarray):
    nan_percent = []
    for i in np.arange(5, len(choices), step=1):
        nan_count = 0
        for j in np.arange(i-5, i, step=1):
            if choices[j] == -1:
                nan_count += 1
        nan_percent.append(float(nan_count) / 5.0)
    return nan_percent


def get_performance(choices: np.ndarray, leftP: np.ndarray):
    adv = choices[choices == 1] and leftP[leftP < 0.5]
    print(adv)
    return sum(adv)


def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)

