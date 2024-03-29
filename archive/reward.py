#This is a manual reward module. This will only work on the PI not on PC. 
# Do not import this module into any scripts. Always use marmocontrol which imports marmoio. 
import RPi.GPIO as GPIO
import time

def deliver():

    PIN_PUMP=13
    PIN_BUZZER=10
    PIN_LED_BLUE=16

    REWARD_VOLUME=500 #may require modification
    REWARD_VOL_FACTOR=0.001 / 3
    BUZZER_LED_TIME=4
    BUZZER_PITCH_CORRECT=800

    DEFAULT_FREQUENCY = 100		# In Hz
    DEFAULT_DUTYCYCLE = 50		# In percentage

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)
    pump = GPIO.PWM(PIN_PUMP, DEFAULT_FREQUENCY)
    pump.start(DEFAULT_DUTYCYCLE)
    buzzer = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_CORRECT)
    buzzer.start(DEFAULT_DUTYCYCLE)
    blueLED = GPIO.PWM(PIN_LED_BLUE, DEFAULT_FREQUENCY)
    blueLED.start(DEFAULT_DUTYCYCLE)
    print(time.ctime())
    time.sleep(3)
    print(time.ctime())
    pump.stop()

    print(time.ctime())
    time.sleep(BUZZER_LED_TIME)
    blueLED.stop()
    buzzer.stop()
    print(time.ctime())
    
    GPIO.cleanup()


if __name__ == '__main__':
    deliver()