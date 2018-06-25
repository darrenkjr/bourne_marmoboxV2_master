# import RPi.GPIO as GPIO
import time
import marmosettings as settings
from marmoio import marmoIO

DEFAULT_FREQUENCY = 100		# In Hz
DEFAULT_DUTYCYCLE = 50		# In percentage

def getParamTrialDelay():
	return settings.TRIAL_DELAY

# For a correct answer a reward is given.
# The BLUE LED, BUZZER and PUMP are activated.
# For the LED and BUZZER ON time, modify BUZZER_LED_TIME in the settings file.
# For the PUMP, modify the values REWARD_VOLUME and REWARD_VOL_FACTOR in the settings file.
def correctAnswer():
	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
	instance.BuzzerCorrect(True)
	instance.BlueLED(True)
	instance.Pump(True)
	# GPIO.setmode(GPIO.BOARD)
	# GPIO.setwarnings(False)
	# GPIO.setup(settings.PIN_LED_BLUE, GPIO.OUT, initial=GPIO.LOW)
	# GPIO.setup(settings.PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
	# GPIO.setup(settings.PIN_PUMP, GPIO.OUT, initial=GPIO.HIGH)

	# buzzer = GPIO.PWM(settings.PIN_BUZZER, settings.BUZZER_PITCH_CORRECT)
	# buzzer.start(0.05)
	# blueLED = GPIO.PWM(settings.PIN_LED_BLUE, DEFAULT_FREQUENCY)
	# blueLED.start(DEFAULT_DUTYCYCLE)
	time.sleep(settings.BUZZER_LED_TIME)
	# blueLED.stop()
	# buzzer.stop()
	instance.BuzzerCorrect(False)
	instance.Pump(False)
	instance.BlueLED(False)
	instance.finish()
	# pump = GPIO.PWM(settings.PIN_PUMP, DEFAULT_FREQUENCY)
	# pump.start(DEFAULT_DUTYCYCLE)
	# time.sleep(settings.REWARD_VOLUME * settings.REWARD_VOL_FACTOR)
	# pump.stop()
	# GPIO.cleanup()

# For an incorrect answer only the GREEN LED and BUZZER are activated.
# The delay time specifies the time both the BUZZER and GREEN LED are ON.
# This value is configurable in the settings file: BUZZER_LED_TIME
def incorrectAnswer():
	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
	instance.GreenLED(marmoIO.On)
	instance.BuzzerIncorrect(marmoIO.On)
	time.sleep(settings.BUZZER_LED_TIME)
	instance.GreenLED(marmoIO.Off)
	instance.buzzIncorrect(marmoIO.Off)
	instance.finish()
	# GPIO.setmode(GPIO.BOARD)
	# GPIO.setwarnings(False)
	# GPIO.setup(settings.PIN_LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
	# GPIO.setup(settings.PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)

	# buzzer = GPIO.PWM(settings.PIN_BUZZER, settings.BUZZER_PITCH_INCORRECT)
	# buzzer.start(DEFAULT_DUTYCYCLE)
	# greenLED = GPIO.PWM(settings.PIN_LED_GREEN, DEFAULT_FREQUENCY)
	# greenLED.start(DEFAULT_DUTYCYCLE)
	# time.sleep(settings.BUZZER_LED_TIME)
	# greenLED.stop()
	# buzzer.stop()
	# GPIO.cleanup()

# This function returns the state of the beam breaker as a True/False value.
def readBeam():
	instance = marmoIO(settings.PIN_LED_BLUE,settings.PIN_LED_GREEN,settings.PIN_BUZZER,settings.PIN_PUMP,settings.PIN_BEAM,settings.BUZZER_PITCH_CORRECT,settings.BUZZER_PITCH_INCORRECT,DEFAULT_DUTYCYCLE)
	# GPIO.setmode(GPIO.BOARD)
	# GPIO.setwarnings(False)
	# GPIO.setup(settings.PIN_BEAM, GPIO.IN)
	# return GPIO.input(settings.PIN_BEAM)
	return instance.readBeam()
