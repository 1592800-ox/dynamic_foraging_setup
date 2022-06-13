import tools.pymysql as mysql

# Creating connection
db = mysql.connect('dynamic-foraging-data.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', 'admin', 'Luph65588590-')
cursor = db.cursor()

# TODO: sort out primary key composition (https://www.simplilearn.com/tutorials/sql-tutorial/composite-key-in-sql)