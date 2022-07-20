# avoiding dsp issue for now
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
from time import sleep
from time import perf_counter
import collections
import pandas as pd
import matplotlib.pyplot as plt
from hardware.modules.mice_ui import Block_UI
import hardware.modules.mice_ui as mice_ui
from hardware.modules.pump_ctrl import Pump
#from analysis.monitor import monitor_train
import seaborn as sns
from hardware.modules.setup import setup
import numpy as np
import RPi.GPIO as GPIO
import pygame
from database.queries import upload_session
import database.tools.pymysql as mysql
import database.queries
from analysis.monitor import monitor_train


# variables storing trial data
MOTOR_REWARD =  0.9
reward_prob = np.array([0.9, 0.9])
choices = []
left_P = []
right_P = []
trial_indices = []
rewarded = []
reaction_time = []
moving_speed = []
# choice made in a trial, left is 0 and right is 1
choice = 0
# advantageous side, 1 is right, 0 is left
adv = 0
# trial index
trial_ind = 0
# number of movement in trial interval, used to determine whether the trial should start
movement = 0
# number of movement during a trial
trial_movement = 0
# Control a mice session with loaded probability file 
IN_A = 17
IN_B = 5
IN_A_FALL = 6
# IN_B_FALL = 26
OUT_REWARD = 26
# seconds before a trial times out and we get a NaN trial
TIME_OUT = 7
# Flag indicating whether we are in the middle of a trial or not
in_trial = False
# ensure only one choice is stored
choice_made = False
partial_left = False
partial_right = False

GPIO.setmode(GPIO.BCM)
# Setup input and output pins with GPIO
GPIO.setup(IN_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_A_FALL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT_REWARD, GPIO.OUT, initial=GPIO.LOW)

fig, axes = plt.subplots(2, 1, figsize=(16, 8))
axes[0].set_ylim([-0.1, 1.3])
axes[1].set_ylim([-0.1, 1.3])
pump = Pump(OUT_REWARD)
print('start setup')
mouse_code, motor_train, train = setup(pump)
print('finished setup')

train = True

block = Block_UI()


# callback functions for GPIO
def callback_rise(callback):
    global partial_left, partial_right

    if not GPIO.input(IN_B):
        partial_right = True
    else:
        partial_left = True


def callback(callback):
    global in_trial, choice, movement, trial_movement, partial_left, choice_made, partial_right

    if GPIO.input(IN_B) and partial_right:
        # B is leading
        if in_trial:
            if not choice_made:
                trial_movement += 1
                if block.update_right(in_trial):
                    #in_trial = False
                    print('chose right')
                    # chose left
                    choice = 1
                    choice_made=True
        else: # trial interval
            movement += 1
    elif not GPIO.input(IN_B) and partial_left:
        if in_trial:
            if not choice_made:
                if block.update_left(in_trial):
                    #in_trial = False
                    print('chose left')
                    # chose right
                    choice = 0
                    choice_made=True
        else: # trial interval
            movement += 1
    partial_right = False
    partial_left = False

GPIO.add_event_detect(IN_A, GPIO.RISING, callback=callback_rise) 
GPIO.add_event_detect(IN_A_FALL, GPIO.FALLING, callback=callback) 

print('added event detection')

if motor_train:
    print('motor training')
    # reward prob for motor training
    reward_prob[0] = MOTOR_REWARD
    reward_prob[1] = MOTOR_REWARD
else:
    adv = np.random.binomial(1, 0.5)
    reward_prob[adv] = np.random.uniform(low=0.85, high=0.95, size=1)
    reward_prob[abs(1-adv)] = 1 - reward_prob[adv]

if train or motor_train:
    print('trianing starts')
    # percentage of the animal choosing the more advantagous side in the past twenty trials
    last_twenty = collections.deque(20*[0], 20)
    
    # trial continues until stopped
    while True:
        print(reward_prob)
        # stop the system bring up not responding window
        pygame.event.pump()
        # random trial interval
        sleep(np.random.randint(1, 4))

        # TODO: test adjusting reward_prob based on past performance
        if not motor_train and sum(collections.Counter(last_twenty)) > 5:
            print('switch prob')
            adv = abs(1 - adv)
            reward_prob[adv] = np.random.uniform(low=0.85, high=0.95, size=1)
            reward_prob[abs(1-adv)] = 1 - reward_prob[adv]

        # a trial doesn't start until the animal stop moving the wheel for 0.5s
        while True:
            movement = 0
            # TODO: test if sleep stops listening for callback as well
            sleep(0.5)
            if movement < 5:
                break

        block.draw()

        start_time = perf_counter()
        choice = -1
        in_trial = True
        choice_made = False
        trial_movement = 0
        print('trial starts')
        # Trial continues until the mouse made a choice or timeout
        while in_trial:
            if choice != -1:
                print('choice made')
                reaction_time.append(perf_counter() - start_time)
                if np.random.binomial(1, reward_prob[choice]):
                    # if given reward
                    pump.send_reward()
                    rewarded.append(1)
                    print('rewarded')
                else:
                    rewarded.append(0)
                # chosen the advantageous side
                last_twenty.append(int(adv == choice))
                block.reset()
                in_trial = False
                break
            block.draw()
            if perf_counter() - start_time > TIME_OUT:
                # no reward for nan trials either
                rewarded.append(0)
                reaction_time.append(-1)
                last_twenty.append(0)
                in_trial = False
                block.reset()
                block.window.fill(mice_ui.BG_COLOR)
                pygame.display.flip()
                break
        moving_speed.append(trial_movement)
        block.reset()
        # store trial data
        trial_indices.append(trial_ind)
        left_P.append(reward_prob[0])
        right_P.append(reward_prob[1])
        choices.append(choice)
        print(last_twenty)
        # next trial
        trial_ind += 1
        # TODO finish training monitoring
        monitor_train(left_p=left_P, right_p=right_P, fig=fig, axes=axes, trial_indices=trial_indices, choices=choices, rewarded=rewarded)
        plt.show(block=False)
        plt.pause(1)
else:
    pass

# TODO add database upload, try and except
# Creating connection
db = mysql.connect(host='dynamic-foraging.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', user='admin', password='Luph65588590-', port=3306, db='dynamic_foraging_data')
cursor = db.cursor()