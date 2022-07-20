from matplotlib import table
import numpy as np
from numpy.typing import NDArray
import pandas as pd
import tools.pymysql as mysql

# initializes the tables
def init(cursor: mysql.connections.Cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    if not ('mice',) in tables:
        create_mice = "CREATE TABLE mice(mouse_code VARCHAR(255), date_of_birth DATE, trained boolean, trained_date DATE, dementia boolean);"
        cursor.execute(create_mice)

    if not ('sessions',) in tables:
        create_mouse_trial = "CREATE TABLE sessions(mouse_code VARCHAR(255), date DATE, prob_set integer, trial_num integer, reward_num integer, nan_trial_num integer, training boolean, motor_training boolean,  CONSTRAINT session_id PRIMARY KEY (mouse_code, date));"
        cursor.execute(create_mouse_trial)

    if not ('trials',) in tables:
        create_trials = "CREATE TABLE trials(mouse_code VARCHAR(255), date DATE, trial_indices integer, left_P double, right_P double, rewarded integer, reaction_time double, moving_speed double, CONSTRAINT session_id PRIMARY KEY (mouse_code, date))"
        cursor.execute(create_trials)

#------------------------------ UPLOAD DATA --------------------------------------------------#
def upload_session(mouse_code, date, prob_set: int, choices: NDArray, rewarded: NDArray, training: bool, motor_training: bool, trial_indices, left_P, right_P, reaction_time, moving_speed, cursor: mysql.connections.Cursor):
    # TODO add session to sessions
    session_query = '''
    INSERT INTO sessions(mouse_code, date, prob_set, trial_num, reward_num, nan_trial_num, training, motor_training) VALUES (%s, %s, %d, %d, %d, %d, %b, %b)
    ''' % (mouse_code, date, prob_set, len(choices), len(rewarded[rewarded==1]), len(choices[choices==-1]), training, motor_training)

    cursor.execute(session_query)
    
    #TODO upload to trials:
    trial_num = len(trial_indices)
    data = pd.DataFrame(list(zip(trial_indices, left_P, right_P, choices, rewarded, reaction_time, moving_speed)), columns=['trial_indices', 'left_P', 'right_P', 'choices', 'rewarded', 'reaction_time', 'moving_speed'])

#-------------------------------- TABLE MODIFICATION -----------------------------------------#
def check_session_exist(date, mouse_code, cursor: mysql.connections.Cursor):
    # TODO query if an entry of a trial exists using the composite primary key
    query = '''
    SELECT * FROM sessions WHERE session_id = (%s, %s)''' % (date, mouse_code)
    cursor.execute(query)
    # returns True if no session matches
    return len(cursor.fetchall()) == 0


def add_column(table_name, column_name, data_type, cursor: mysql.connections.Cursor):
    query = '''
        ALTER TABLE %s
        ADD %s %s''' % (table_name, column_name, data_type)
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False

#----------------------------------------- DANGER ZONE ----------------------------------------#
def delete_table(table_name, cursor: mysql.connections.Cursor):
    query = '''
    DROP TABLE %s''' % table_name
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False

def delete_all(cursor: mysql.connections.Cursor):
    query = '''
    DROP TABLE  mice, sessions, trials'''
    try:
        cursor.execute(query)
        return True
    except Exception:
        return False