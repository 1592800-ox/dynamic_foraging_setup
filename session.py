# avoiding dsp issue for now
import collections
import os
from time import perf_counter, sleep

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygame
import RPi.GPIO as GPIO
#from analysis.monitor import monitor_train
import seaborn as sns

import database.queries
import database.tools.pymysql as mysql
import hardware.modules.mice_ui as mice_ui
from analysis.monitor import monitor_train
from database.queries import upload_session
from hardware.modules.mice_ui import Block_UI
from hardware.modules.pump_ctrl import Pump
from hardware.modules.setup import setup

# TODO sort out the variables 
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
# enure only one choice is stored
choice_made = False
partial_left = False
partial_right = False
TRIAL_NUM = 0

Encoder_A = 0
Encoder_A_old = 0
Encoder_B = 0
Encoder_B_old = 0

# probability limits
MOTOR = 0.85

GPIO.setmode(GPIO.BCM)
# Setup input and output pins with GPIO
GPIO.setup(IN_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT_REWARD, GPIO.OUT, initial=GPIO.LOW)

fig, axes = plt.subplots(2, 1, figsize=(16, 8))
axes[0].set_ylim([-0.1, 1.3])
axes[1].set_ylim([-0.1, 1.3])
pump = Pump(OUT_REWARD)
print('start setup')
code, mode = setup(pump)
print('finished setup')

train = True

block = Block_UI()
pygame.mixer.init(400000)
beep = pygame.mixer.Sound('beep-07a.wav')


def quadrature_decode(callback):
    global Encoder_A
    global Encoder_A_old
    global Encoder_B
    global Encoder_B_old
    global in_trial
    global movement
    global choice_made
    global trial_movement
    global block
    global choice

    Encoder_A = GPIO.input(IN_A)
    Encoder_B = GPIO.input(IN_B)

    if (Encoder_A == 1 and Encoder_B_old == 0) or (Encoder_A == 0 and Encoder_B_old == 1):
        # this will be clockwise rotation
        if in_trial:
            if not choice_made:
                trial_movement += 1
                if block.update_right(in_trial):
                    #in_trial = False
                    print('chose right')
                    # chose right
                    choice = 1
                    choice_made=True
        else: # trial interval
            movement += 1

    elif (Encoder_A == 1 and Encoder_B_old == 1) or (Encoder_A == 0 and Encoder_B_old == 0):
        # this will be counter-clockwise rotation
        if in_trial:
            if not choice_made:
                trial_movement += 1
                if block.update_left(in_trial):
                    #in_trial = False
                    print('chose left')
                    # chose left
                    choice = 0
                    choice_made=True
        else: # trial interval
            movement += 1
        
    Encoder_A_old = Encoder_A   
    Encoder_B_old = Encoder_B       

GPIO.add_event_detect(IN_A, GPIO.BOTH, callback=quadrature_decode) 
GPIO.add_event_detect(IN_B, GPIO.BOTH, callback=quadrature_decode) 

print('added event detection')

if mode == 'motor_training':
    print('motor training')
    # reward prob for motor training
    reward_prob[0] = MOTOR_REWARD
    reward_prob[1] = MOTOR_REWARD
    TRIAL_NUM = 300

if mode == 'training_1' or mode == 'training_2':
    adv = np.random.binomial(1, 0.5)
    reward_prob[adv] = np.random.uniform(low=0.85, high=0.95, size=1)
    reward_prob[abs(1-adv)] = 1 - reward_prob[adv]
    if mode == 'training_1':
        TRIAL_NUM = 350
    else:
        TRIAL_NUM = 450

if mode != 'data_collection':
    # number of trials spend on the current block
    curr_block = 0
    # percentage of the animal choosing the more advantagous side in the past twenty trials
    last_twenty = collections.deque(20*[0], 20)
    
    # trial continues until stopped
    while True:
        print(reward_prob)
        # stop the system bring up not responding window
        pygame.event.pump()
        # random trial interval
        sleep(np.random.randint(1, 4))

        # block switch in trianing mode
        if mode != 'motor_training' and last_twenty.count(1) > 15 and curr_block > 40:
            print('switch prob')
            adv = abs(1 - adv)
            reward_prob[adv] = np.random.uniform(low=0.85, high=0.95, size=1)
            reward_prob[abs(1-adv)] = 1 - reward_prob[adv]
            last_twenty = collections.deque(20*[0], 20)

        # next trial doesn't start until the animal stop moving the wheel for 0.5s
        while True:
            movement = 0
            sleep(0.5)
            if movement < 5:
                break
        beep.play()
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
        print(sum(collections.Counter(last_twenty)) )
        # next trial
        trial_ind += 1

        monitor_train(left_p=left_P, right_p=right_P, axes=axes, trial_indices=trial_indices, choices=choices, rewarded=rewarded)
        plt.show(block=False)
        plt.pause(0.1)
else:
    pass

# Creating connection
config = {
    'host': 'dynamic-foraging-mysql.mysql.database.azure.com',
    'user': 'peiheng',
    'password': 'Luph65588590-',
    'database': 'dynamic-foraging',
    'client_flags': [mysql.connector.ClientFlag.SSL]
}

# try upload 5 times before giving up
error_counter = 5
uploaded = False

while not uploaded and error_counter >= 0:
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        uploaded = True
    except Exception:
        print('connection error, retry %d time' % error_counter)
        error_counter -= 1


