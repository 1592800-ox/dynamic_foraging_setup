# Fake GPIO allowing the code to compile on windows device

BOARD = 1
OUT = 1
IN = 1
BCM = 1
LOW = 0
PUD_DOWN = 0

def setmode(a):
   print(a)
def setup(a, b):
   print(a)
def output(a, b):
   print(a)
def cleanup():
   print('a')
def setwarnings(flag):
   print('False')