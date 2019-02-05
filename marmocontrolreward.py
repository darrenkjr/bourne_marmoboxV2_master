import time
import marmosettings as settings
import os

# Check if running on Pi
marmobox_env = os.environ.get('marmobox_env') 
if marmobox_env == 'RPI':
	from marmoio import marmoIO
	import marmoio
else: # If not runing on RPi, initiate the simulation module
	from marmoiosim import marmoIO
	import marmoiosim as marmoio

DEFAULT_FREQUENCY = 100		# In Hz
DEFAULT_DUTYCYCLE = 50		# In percentage

def getParamTrialDelay():
	return settings.TRIAL_DELAY

# For a correct answer a reward is given.
# The BLUE LED, BUZZER and PUMP are activated.
# For the LED and BUZZER ON time, modify BUZZER_LED_TIME in the settings file.
# For the PUMP, modify the values REWARD_VOLUME and REWARD_VOL_FACTOR in the settings file.
def correctAnswer(*args):
	if args:
		reward = args[0]
	else:
		reward = True

	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
    
   	if reward:
        	instance.Pump(True)
   	instance.BuzzerCorrect(True)
	instance.BlueLED(True)

	time.sleep(settings.BUZZER_LED_TIME)
	instance.BuzzerCorrect(False)
	instance.Pump(False)
	instance.BlueLED(False)
	instance.finish()


# For an incorrect answer only the GREEN LED and BUZZER are activated.
# The delay time specifies the time both the BUZZER and GREEN LED are ON.
# This value is configurable in the settings file: BUZZER_LED_TIME
def incorrectAnswer():
	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
	instance.GreenLED(marmoIO.On)
	instance.BuzzerIncorrect(marmoIO.On)
	time.sleep(settings.BUZZER_LED_TIME)
	instance.GreenLED(marmoIO.Off)
	instance.BuzzerIncorrect(marmoIO.Off)
	instance.finish()


# This function returns the state of the beam breaker as a True/False value.
def readBeam():
	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
	return instance.readBeam()

def reward():
	marmoio.manual_reward()

def force_stop():
	marmoio.forceStop()
