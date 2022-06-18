# used for modifying the sql databases using the queries defined in queries.py
import tools.pymysql as mysql
import queries

# Creating connection
db = mysql.connect(host='dynamic-foraging.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', user='admin', password='Luph65588590-', port=3306, db='dynamic_foraging_data')
cursor = db.cursor()

# TODO: sort out primary key composition (https://www.simplilearn.com/tutorials/sql-tutorial/composite-key-in-sql)
print('connection established')

cursor.execute(queries.delete_table('mouse_trial'))
