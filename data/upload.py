from tkinter import Tk
from tkinter.filedialog import askdirectory
import tools.pymysql as mysql
import os


def upload_to_rds():
    # upload a csv folder containing the training data for the day
    folder = askdirectory(title='Which folder are we uploading?') # select the csv data folder
    print(folder)
    date = os.path.basename(folder)

    

    # Creating connection
    db = mysql.connect('dynamic-foraging-data.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', 'admin', 'Luph65588590-')
    cursor = db.cursor()

    