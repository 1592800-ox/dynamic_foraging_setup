import numpy as np
from database.queries import upload_session, get_stage
from datetime import date
import mysql.connector

config = {
    'host': 'dynamic-foraging-mysql.mysql.database.azure.com',
    'user': 'peiheng',
    'password': 'Luph65588590-',
    'database': 'dynamic-foraging'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

mouse_code = 'JGED01'
trial_indices = np.arange(0, 60, dtype=int)
leftP_test = [0.1] * 20 + [0.8]*20 + [0.15]*20
rightP_test = [1 - i for i in leftP_test]
choice_test = [1] * 23 + [-1] + [0] * 36 
rewards = [1] * 10 + [0] * 13 + [-1] + [1] * 10 + [0] * 26
reaction_time = np.linspace(1, 5, len(trial_indices))
moving_speed = np.linspace(500, 200, len(trial_indices))
stage = get_stage(mouse_code, cursor)

print(reaction_time)
print(moving_speed)

today = date.today()
today.strftime('%Y/%m/%d')
print(today)

today = '2019/10/11'

upload_session(mouse_code=mouse_code, date=today, stage=stage, prob_set=-3, choices=choice_test, rewarded=rewards, trial_indices=trial_indices, leftP=leftP_test, rightP=rightP_test, reaction_time=reaction_time, moving_speed=moving_speed, cursor=cursor)

db.commit()