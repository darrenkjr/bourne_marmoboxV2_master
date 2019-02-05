#This is a manual reward module. This will only work on the PI not on PC. 
# Do not import this module into any scripts. Always use marmocontrol which imports marmoio. 
import RPi.GPIO as GPIO
import time

def deliver():
    PIN_PUMP=13
    PIN_BUZZER=10
    PIN_LED_BLUE=16
    
    BUZZER_LED_TIME=2.0
    BUZZER_PITCH_CORRECT=800

    DEFAULT_FREQUENCY = 100		# In Hz
    DEFAULT_DUTYCYCLE = 50	# in percentage


    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)

    buzzer = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_CORRECT)
    buzzer.start(DEFAULT_DUTYCYCLE)
    blueLED = GPIO.PWM(PIN_LED_BLUE, DEFAULT_FREQUENCY)
    blueLED.start(DEFAULT_DUTYCYCLE)
    time.sleep(BUZZER_LED_TIME)
    blueLED.stop()
    buzzer.stop()

    pump = GPIO.PWM(PIN_PUMP, DEFAULT_FREQUENCY)
    pump.start(5)
   # time.sleep(REWARD_VOLUME * REWARD_VOL_FACTOR)
    pump.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    deliver()