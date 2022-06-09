from tkinter import Tk
from tkinter.filedialog import askdirectory

folder = askdirectory(title='Which folder are we uploading?') # select the csv data folder

print(folder)