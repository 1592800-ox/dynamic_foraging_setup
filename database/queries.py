import datetime
from distutils.util import execute
from math import nan
from mimetypes import common_types
from operator import indexOf
from sqlite3 import Cursor
from matplotlib import table
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from mysql.connector.cursor import CursorBase

stages = ['motor_training', 'training_1', 'training_2', 'standby']

# initializes the tables
def init(cursor: CursorBase):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print(tables)

    if not ('mice',) in tables:
        create_mice = "CREATE TABLE mice(mouse_code VARCHAR(10) PRIMARY KEY, date_of_birth DATE,  dementia boolean, stage VARCHAR(20) DEFAULT 'motor_training');"
        cursor.execute(create_mice)

    if not ('sessions',) in tables:
        create_mouse_trial = "CREATE TABLE sessions(mouse_code VARCHAR(10), FOREIGN KEY (mouse_code) REFERENCES mice (mouse_code), date DATE, prob_set integer, trial_num integer, reward_num integer, nan_trial_num integer, CONSTRAINT session_id PRIMARY KEY (mouse_code, date));"
        cursor.execute(create_mouse_trial)

    if not ('trials',) in tables:
        create_trials = "CREATE TABLE trials(mouse_code VARCHAR(10), date DATE, CONSTRAINT session_id FOREIGN KEY (mouse_code, date) REFERENCES sessions(mouse_code, date), trial_index integer, leftP double, rightP double, choices integer, rewarded integer, reaction_time double, moving_speed double, CONSTRAINT trial_id PRIMARY KEY (mouse_code, date, trial_index))"
        cursor.execute(create_trials)

#------------------------------ UPLOAD DATA --------------------------------------------------#
def upload_session(mouse_code, date, stage, prob_set: int, choices: NDArray, rewarded: NDArray, trial_indices, leftP, rightP, reaction_time, moving_speed, cursor: CursorBase):
    # TODO add session to sessions
    trial_num = len(trial_indices)
    print(rewarded == 1)
    reward_num = sum([reward == 1 for reward in rewarded])
    nan_trial_num = np.sum([choice == -1 for choice in choices])
    
    query = '''
        INSERT INTO sessions (mouse_code, date, prob_set, trial_num, reward_num, nan_trial_num) VALUES 
        ('%s', '%s', %d, %d, %d, %d)
        ''' % (mouse_code, date, prob_set, trial_num, reward_num, nan_trial_num)
    
    cursor.execute(query)

    for ind in range(trial_num):
        query = '''
            INSERT INTO trials (mouse_code, date, trial_index, leftP, rightP, choices, rewarded, reaction_time, moving_speed) 
            VALUES ('%s', '%s', %d, %f, %f, %d, %d, %f, %f) 
            ''' % (mouse_code, date, trial_indices[ind], leftP[ind], rightP[ind], choices[ind], rewarded[ind], reaction_time[ind], moving_speed[ind])
        cursor.execute(query)
        

#-------------------------------- TABLE MODIFICATION -----------------------------------------#
def add_animal(mouse_code: str, date_of_birth: str, cursor: CursorBase):
    query = '''
        INSERT INTO mice (mouse_code, date_of_birth) VALUES ('%s', '%s')
        ''' % (mouse_code, date_of_birth)
    try:
        cursor.execute(query)
    except Exception:
        return False
    return True

def get_animals(cursor: CursorBase):
    query = '''
        SELECT mouse_code FROM mice
        '''
    cursor.execute(query)
    mice = cursor.fetchall()
    return [i[0] for i in mice]

def check_session_exist(date: str, mouse_code: str, cursor: CursorBase):
    # TODO query if an entry of a trial exists using the composite primary key
    query = '''
    SELECT * FROM sessions WHERE session_id = ('%s','%s')''' % (date, mouse_code)
    cursor.execute(query)
    print(query)
    # returns True if no session matches
    return len(cursor.fetchall()) == 0


def add_column(table_name, column_name, data_type, cursor: CursorBase):
    query = '''
        ALTER TABLE %s
        ADD %s %s''' % (table_name, column_name, data_type)
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False

def get_stage(mouse_code: str, cursor: CursorBase):
    query = '''
        SELECT stage 
        FROM mice
        WHERE mouse_code = '%s';
        ''' % (mouse_code)
    cursor.execute(query)
    return cursor.fetchall()[0][0]

def get_age(mouse_code:str, cursor: CursorBase):
    query = '''
        SELECT date_of_birth 
        FROM mice
        WHERE mouse_code = '%s';
        ''' % (mouse_code)
    cursor.execute(query)
    dob = cursor.fetchall()[0][0]
    today = datetime.date.today()
    return (today - dob).days


def next_stage(mouse_code: str, cursor: CursorBase, stage=None):
    if stage == None:
        stage = get_stage(mouse_code, cursor)
    curr_stage = stages.index(stage)
    if curr_stage == len(stages) - 1:
        print('already at final stage')
        return False
    next_stage = stages[curr_stage + 1]
    query = '''
        UPDATE mice
        SET stage = '%s'
        WHERE mouse_code = '%s'
        ''' % (next_stage, mouse_code)
    cursor.execute(query)

def start_collect(mouse_code: str, cursor: CursorBase):
    next_stage = '0'
    query = '''
        UPDATE mice
        SET stage = '%s'
        WHERE mouse_code = '%s'
        ''' % (next_stage, mouse_code)
    cursor.execute(query)

def next_set(mouse_code: str, set: int, cursor: CursorBase):
    next_stage = str(set + 1)
    query = '''
        UPDATE mice
        SET stage = '%s'
        WHERE mouse_code = '%s'
        ''' % (next_stage, mouse_code)
    cursor.execute(query)

#----------------------------------------- DANGER ZONE ----------------------------------------#
def delete_table(table_name, cursor: CursorBase):
    query = '''
    DROP TABLE %s''' % table_name
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False

def delete_all(cursor: CursorBase):
    query = '''
    SET FOREIGN_KEY_CHECKS = 0;
    drop table if exists mice;
    drop table if exists sessions;
    drop table if exists trials;
    SET FOREIGN_KEY_CHECKS = 1;'''
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False