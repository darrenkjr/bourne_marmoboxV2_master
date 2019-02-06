#This is a manual reward module. This will only work on the PI not on PC. 
# Do not import this module into any scripts. Always use marmocontrol which imports marmoio. 
import RPi.GPIO as GPIO
import time

def deliver():
    iterations = 0
    while iterations <= 5:

        PIN_LED_GREEN=18

        BUZZER_LED_TIME=2.0

        DEFAULT_FREQUENCY = 100		# In Hz
        DEFAULT_DUTYCYCLE = 50		# In percentage

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)


    greenLED = GPIO.PWM(PIN_LED_GREEN, DEFAULT_FREQUENCY)
    greenLED.start(DEFAULT_DUTYCYCLE)
    time.sleep(BUZZER_LED_TIME)
    greenLED.stop()

    GPIO.cleanup()
    iterations += 1


if __name__ == '__main__':
    deliver()