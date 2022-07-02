from matplotlib import table
import numpy as np
from numpy.typing import NDArray
import pandas as pd
import database.tools.pymysql as mysql


#------------------------------ UPLOAD DATA --------------------------------------------------#
def upload_to_session(mouse_code, date, prob_set: int, choices: NDArray, rewarded: NDArray, trial_ind: NDArray, training: bool, motor_training: bool, cursor: mysql.connections.Cursor):
    # TODO add session to sessions
    session_query = '''
    INSERT INTO sessions(mouse_code, date, prob_set, trial_num, reward_num, nan_trial_num, training, motor_training) VALUES (%s, %s, %d, %d, %d, %d, %b, %b)
    ''' % (mouse_code, date, prob_set, len(choices), len(rewarded[rewarded==1]), len(choices[choices==-1]), training, motor_training)

    cursor.execute(session_query)
    # TODO add trials to the trials table
    
    

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