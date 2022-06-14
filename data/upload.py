from tkinter import Tk
from tkinter.filedialog import askdirectory
import tools.pymysql as mysql
import os


def upload_to_rds(path):
    # upload a csv file containing the training data
    

    # Creating connection
    db = mysql.connect('dynamic-foraging-data.cqmwfsljtplu.eu-west-2.rds.amazonaws.com', 'admin', 'Luph65588590-')
    cursor = db.cursor()

    