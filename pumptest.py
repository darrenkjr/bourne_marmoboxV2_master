# Do not import this module into any scripts.

import RPi.GPIO as GPIO
import time

def deliver():

    PIN_PUMP=13
    PIN_BUZZER=10
    PIN_LED_BLUE=16

    BUZZER_PITCH_CORRECT=800

    DEFAULT_FREQUENCY = 100		# In Hz
    DEFAULT_DUTYCYCLE = 50		# In percentage
    PUMP_DUTYCYCLE = 5

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)

    buzzer = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_CORRECT)
    buzzer.start(DEFAULT_DUTYCYCLE)
    blueLED = GPIO.PWM(PIN_LED_BLUE, DEFAULT_FREQUENCY)
    blueLED.start(DEFAULT_DUTYCYCLE)

    pump = GPIO.PWM(PIN_PUMP, 7000)
    pump.start(PUMP_DUTYCYCLE)
   
    time.sleep(2)

    GPIO.cleanup()


if __name__ == '__main__':
    deliver()