from mysql.connector import connect

mydb = connect(host='localhost', user='root', passwd='Luph65588590-')

mycursor = mydb.cursor()

mycursor.execute('show databases')

for i in mycursor:
    print(i)