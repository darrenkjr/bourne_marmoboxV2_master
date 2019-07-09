import RPi.GPIO as GPIO
import time
from archive import marmosettings as settings

GPIO.setmode(GPIO.BOARD)
GPIO.setup(settings.PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)
time.sleep(15)
GPIO.setup(settings.PIN_PUMP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.cleanup()

#jack