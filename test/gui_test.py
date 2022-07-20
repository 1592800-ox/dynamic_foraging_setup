import os, sys
sys.path.insert(0, os.path.abspath('..'))
from hardware.modules.setup import setup
from hardware.modules.pump_ctrl import Pump

code, motor_training, training = setup(Pump(999))