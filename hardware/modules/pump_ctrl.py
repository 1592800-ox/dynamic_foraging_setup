from time import sleep
import RPi.GPIO as GPIO

class Pump:
    def __init__(self, reward_pin) -> None:
        self.pin = reward_pin        

    # quick pulse to the pump
    def send_reward(self):
        GPIO.output(self.pin, 1)
        sleep(0.1)
        GPIO.output(self.pin, 0)

    def open_valve(self):
        GPIO.output(self.pin, 1)

    def close_valve(self):
        GPIO.output(self.pin, 0)