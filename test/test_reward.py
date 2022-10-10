from time import sleep
from hardware.modules.pump_ctrl import Pump
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)


pump = Pump(26)

for i in range(100):
    pump.send_reward('motor')
    sleep(0.5)
