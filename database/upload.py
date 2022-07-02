from secrets import choice
from tkinter import Tk
from tkinter.filedialog import askdirectory
import database.tools.pymysql as mysql
import os
import pandas as pd
from database import queries
from datetime import date


def upload_to_rds(data: pd.DataFrame, mouse_code, training, motor_training, cursor: mysql.connections.Cursor):
    today = date.today().strftime('%Y-%m-%d')
    choices = data['choices']
    rewarded = data['rewarded']
    trial_indices = data['trial_indices']
    left_prob = data['left_prob']
    right_prob = data['right_prob']
    # upload a dataframe containing the training data
    if queries.check_session_exist(date=today, mouse_code=mouse_code, cursor=cursor):
        print('the session is already recorded')
        return
    if not queries.upload_to_session(mouse_code, today, -1, trial_num=choices.size, reward_num=rewarded.sum(), nan_trial_num=choices.isna().sum(), training=training, motor_training=motor_training):
        print('error uploading session data')
        return
    
    