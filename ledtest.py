#This script tests LED function. If working, LEDs will flash every 15 seconds over 5 iterations. The buzzer will sound when the LEDs are meant to activate.

import RPi.GPIO as GPIO
import time

def deliver():
    iterations = 0
    while iterations <= 5:

        PIN_BUZZER=10
        PIN_LED_GREEN=18
        PIN_LED_BLUE=16

        BUZZER_LED_TIME=2.0
        BUZZER_PITCH_CORRECT=600

        DEFAULT_FREQUENCY = 100		# In Hz
        DEFAULT_DUTYCYCLE = 50		# In percentage

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)

        buzzer = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_CORRECT)
        buzzer.start(DEFAULT_DUTYCYCLE)
        greenLED = GPIO.PWM(PIN_LED_GREEN, DEFAULT_FREQUENCY)
        blueLED = GPIO.PWM(PIN_LED_BLUE, DEFAULT_FREQUENCY)
        blueLED.start(DEFAULT_DUTYCYCLE)
        greenLED.start(DEFAULT_DUTYCYCLE)
        time.sleep(BUZZER_LED_TIME)

        GPIO.cleanup()
        time.sleep(15)
        iterations +=1


if __name__ == '__main__':
    deliver()