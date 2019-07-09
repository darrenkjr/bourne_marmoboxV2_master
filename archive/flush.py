import RPi.GPIO as GPIO
from archive import marmosettings as settings

GPIO.setmode(GPIO.BOARD)
GPIO.setup(settings.PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)
#time.sleep(3)
x = raw_input('Press any key to stop')
GPIO.setup(settings.PIN_PUMP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.cleanup()
