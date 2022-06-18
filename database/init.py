# initilzes the tables needed by us
import tools.pymysql as mysql

# Creating connection
db = mysql.connect(host='dynamic-foraging.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', user='admin', password='Luph65588590-', port=3306, db='dynamic_foraging_data')
cursor = db.cursor()

# TODO: sort out primary key composition (https://www.simplilearn.com/tutorials/sql-tutorial/composite-key-in-sql)
print('connection established')

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

if not ('mice',) in tables:
    create_mice = "CREATE TABLE mice(mouse_code VARCHAR(255), date_of_birth DATE, trained boolean, trained_date DATE, dementia boolean);"
    cursor.execute(create_mice)
    db.commit()

if not ('sessions',) in tables:
    create_mouse_trial = "CREATE TABLE sessions(mouse_code VARCHAR(255), date DATE, prob_set integer, trial_num integer, reward_num integer, nan_trial_num integer, training boolean, motor_training boolean);"
    cursor.execute(create_mouse_trial)
    db.commit()

if not ('trials',) in tables:
    create_trials = "CREATE TABLE trials(mouse_code VARCHAR(255), date DATE, trial_index integer, left_prob double, right_prob double, rewarded boolean, reaction_time double, moving_speed double, CONSTRAINT session_id PRIMARY KEY (mouse_code, date))"
    cursor.execute(create_trials)
    db.commit()