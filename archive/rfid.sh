#! /bin/bash

read -t $1 X < /dev/ttyUSB0 
if [ -z "$X" ] 
then
	echo "no rfid"
else
	echo $X
fi


