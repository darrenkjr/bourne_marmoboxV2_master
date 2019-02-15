import RPi.GPIO as GPIO
import time
class marmoIO:
    On = True
    Off = False
    def __init__(self,PIN_LED_BLUE,PIN_LED_GREEN,PIN_BUZZER,PIN_PUMP,PIN_BEAM,BUZZER_PITCH_CORRECT,BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(PIN_BEAM, GPIO.IN)
        self.PIN_BUZZER = PIN_BUZZER
        self.BUZZER_PITCH_CORRECT = BUZZER_PITCH_CORRECT
        self.BUZZER_PITCH_INCORRECT = BUZZER_PITCH_INCORRECT
        self.PIN_LED_GREEN = PIN_LED_GREEN
        self.PIN_LED_BLUE = PIN_LED_BLUE
        self.PIN_PUMP = PIN_PUMP
        self.PIN_BEAM = PIN_BEAM
        self.DEFAULT_DUTYCYCLE = DEFAULT_DUTYCYCLE
        
    def BuzzerCorrect(self,state):
        if state:
            self.buzzCorrect = GPIO.PWM(self.PIN_BUZZER, self.BUZZER_PITCH_CORRECT)
            self.buzzCorrect.start(self.DEFAULT_DUTYCYCLE)
        else:
            self.buzzCorrect.stop()
        
    def BuzzerIncorrect(self,state):
        if state:
            self.buzzIncorrect = GPIO.PWM(self.PIN_BUZZER, self.BUZZER_PITCH_INCORRECT)
            self.buzzIncorrect.start(self.DEFAULT_DUTYCYCLE)
        else:
            self.buzzIncorrect.stop()
        
    def Pump(self,state):
        GPIO.output(self.PIN_PUMP,GPIO.LOW if state else GPIO.HIGH)

    def GreenLED(self,state): #State is either 1 on or 0 off
            GPIO.output(self.PIN_LED_GREEN,GPIO.HIGH if state else GPIO.LOW)

    def BlueLED(self,state): #State is either 1 on or 0 off
        GPIO.output(self.PIN_LED_BLUE,GPIO.HIGH if state else GPIO.LOW)

    def readBeam(self):
        val = GPIO.input(self.PIN_BEAM)
        return val

    def finish(self):
        GPIO.cleanup()

def forceStop(): # Force stop a run-away pump
    PIN_PUMP=13
    DEFAULT_FREQUENCY = 100		# In Hz
    GPIO.setmode(GPIO.BOARD)
    pump = GPIO.PWM(PIN_PUMP, DEFAULT_FREQUENCY)
    pump.stop()

def manual_reward():
    PIN_PUMP=13
    PIN_BUZZER=10
    PIN_LED_BLUE=16

    REWARD_VOLUME=500 #may require modification
    REWARD_VOL_FACTOR=0.001 / 3
    BUZZER_LED_TIME=2.0
    BUZZER_PITCH_CORRECT=800

    DEFAULT_FREQUENCY = 100		# In Hz
    DEFAULT_DUTYCYCLE = 50		# In percentage

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
    pump.start(DEFAULT_DUTYCYCLE)
    time.sleep(REWARD_VOLUME * REWARD_VOL_FACTOR)
    pump.stop()
    GPIO.cleanup()