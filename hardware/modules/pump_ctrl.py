from time import sleep
import RPi.GPIO as GPIO

class Pump:
    def __init__(self, reward_pin) -> None:
        self.pin = reward_pin        

    # quick pulse to the pump
    def send_reward(self, mode):
        GPIO.output(self.pin, 1)
        if 'motor' in mode:
            print('motor reward')
            sleep(0.08)
        else:
            sleep(0.1)
        GPIO.output(self.pin, 0)

    def open_valve(self):
        GPIO.output(self.pin, 1)

    def close_valve(self):
        GPIO.output(self.pin, 0)