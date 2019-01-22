# Simulator Library for Marmobox I/O Operations. 
# Includes control of pump, lights and beambreaker

class marmoIO:
    On = True
    Off = False
    def __init__(self,PIN_LED_BLUE,PIN_LED_GREEN,PIN_BUZZER,PIN_PUMP,PIN_BEAM,BUZZER_PITCH_CORRECT,BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE):
        # print 'Buzzer GPIO Pin: ' + str(PIN_BUZZER )
        # print 'Buzzer Pitch incorrect: '+str(BUZZER_PITCH_INCORRECT)
        # print 'Buzzer Pitch correct: ' + str(BUZZER_PITCH_CORRECT)
        self.PIN_LED_GREEN = PIN_LED_GREEN
        self.PIN_LED_BLUE = PIN_LED_BLUE
        self.PIN_PUMP = PIN_PUMP
        self.PIN_BEAM = PIN_BEAM
        self.DEFAULT_DUTYCYCLE = DEFAULT_DUTYCYCLE
        
    def BuzzerCorrect(self,state):
        if state:
	        print('Correct Buzzer On with Duty Cycle: ' + str(self.DEFAULT_DUTYCYCLE))
        else:
            print('Correct Buzzer Off')
        
    def BuzzerIncorrect(self,state):
        if state:
            print('Incorrect Buzzer On with Duty Cycle: ' + str(self.DEFAULT_DUTYCYCLE))
        else:
            print('Incorrect Buzzer Off')
        
    def Pump(self,state):
        if state:
            print('Pump On')
        else:
            print('Pump Off')
        # print 'Pin: ' + str(self.PIN_PUMP)

    def GreenLED(self,state): #State is either 1 on or 0 off
        if state:
            print('GreenLED On')
        else:
            print('GreenLED Off')
        # print 'Pin: ' + str(self.PIN_PUMP)

    def BlueLED(self,state): #State is either 1 on or 0 off
        if state:
            print('BlueLED On')
        else:
            print('BlueLED Off')
        # print 'Pin: ' + str(self.PIN_PUMP)

    def readBeam(self):
        val = raw_input('Press any key then Enter/Return to continue')
        return False if str(val) else True

    def finish(self):
        print('Clean GPIO State')

def forceStop():
    print('Force Pump Stop')

def manual_reward():
    print('Delivered manual reward')