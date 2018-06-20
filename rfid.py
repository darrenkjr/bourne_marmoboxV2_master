#!/usr/bin/env python
import time
import serial
device = serial.Serial(
	port="/dev/ttyUSB0", 
	baudrate=9600, 
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)

#device.write('VER\r')
#print device.readline()
device.write('ST2\r')
z = 1
while z:
	device.readline()
	z = 0
y = 1
while y:
	x = device.readline()
	if x != '':
		print x
		y = 0
