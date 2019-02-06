#This is a manual reward module. This will only work on the PI not on PC. 
# Do not import this module into any scripts. Always use marmocontrol which imports marmoio. 
import RPi.GPIO as GPIO
import time

def deliver():
    while iterations <= 5
        PIN_PUMP=13
        PIN_BUZZER=10
        PIN_LED_GREENB=18

        REWARD_VOLUME=500 #may require modification
        REWARD_VOL_FACTOR=0.001 / 3
        BUZZER_LED_TIME=2.0
        BUZZER_PITCH_CORRECT=800

        DEFAULT_FREQUENCY = 100		# In Hz
        DEFAULT_DUTYCYCLE = 50		# In percentage

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)


    greenLED = GPIO.PWM(PIN_LED_GREEN, DEFAULT_FREQUENCY)
    greenLED.start(DEFAULT_DUTYCYCLE)
    time.sleep(BUZZER_LED_TIME)
    greenLED.stop()
    buzzer.stop()

    GPIO.cleanup()


if __name__ == '__main__':
    deliver()