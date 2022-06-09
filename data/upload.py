from tkinter import Tk
from tkinter.filedialog import askdirectory
import pymysql


folder = askdirectory(title='Which folder are we uploading?') # select the csv data folder

print(folder)

# Creating connection
db = pymysql.connect('dynamic-foraging-data.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', 'admin', 'Luph65588590-')
cursor = db.cursor()

cursor.execute('select version()')
