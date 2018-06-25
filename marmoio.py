import RPi.GPIO as GPIO

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
        GPIO.setup(PIN_BEAM, GPIO.IN)
        self.buzzIncorrect = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_INCORRECT)
        self.buzzCorrect = GPIO.PWM(PIN_BUZZER, BUZZER_PITCH_CORRECT)
        self.PIN_LED_GREEN = PIN_LED_GREEN
        self.PIN_LED_BLUE = PIN_LED_BLUE
        self.PIN_PUMP = PIN_PUMP
        self.PIN_BEAM = PIN_BEAM
        self.DEFAULT_DUTYCYCLE = DEFAULT_DUTYCYCLE
        
    def BuzzerCorrect(self,state):
        if state:
	        self.buzzCorrect.start(self.DEFAULT_DUTYCYCLE)
        else:
            self.buzzCorrect.stop()
        
    def BuzzerIncorrect(self,state):
        if state:
            self.buzzIncorrect.start(self.DEFAULT_DUTYCYCLE)
        else:
            self.buzzIncorrect.stop()
        
    def Pump(self,state):
        GPIO.output(self.PIN_PUMP,state)

    def GreenLED(self,state): #State is either 1 on or 0 off
        GPIO.output(self.PIN_LED_GREEN,state)

    def BlueLED(self,state): #State is either 1 on or 0 off
        GPIO.output(self.PIN_LED_BLUE,state)

    def readBeam(self):
        val = GPIO.input(self.PIN_BEAM)
        return val

    def finish(self):
        GPIO.cleanup()