import marmocontrol as control
import argparse
import importlib
import time, datetime
from psychopy import visual, core, logging, event

#alternatively in terminal: python splash.py

def run(taskname, mywin,limitTrial, animal_ID, session):
   # detect marmoset
   print('Attempting to detect ' + animal_ID)

   beamInput = False
   #beamInput = True
   #while beamInput:
   #    time.sleep(0.1)
   #    beamInput = control.readBeam()

   print('Animal found! Now attempting to read RFID tag...')

   # read RFID tag
   # implement with rfid.py
   # launch experiment

   print('Starting task: ' + str(taskname))
   #time.sleep(float(delay))

   code_start = datetime.datetime.now()

   print('Started!')
   task = importlib.import_module(taskname)

   totalTime = task.execTask(taskname,limitTrial,mywin, animal_ID,session)
   code_endtime = (datetime.datetime.now() - code_start).total_seconds()

   print('Task ended, elasped time (less time spent in testing): ' + str(code_endtime - totalTime) + 'seconds')


if __name__ == '__main__':
   # initialise the argument parser
   ap = argparse.ArgumentParser()
   ap.add_argument('-t', '--task', help='name of the task')
   #ap.add_argument('-d', '--delay', help='delay in seconds for executing tasks')
   ap.add_argument('-l', '--limitTrial', help = 'input number of required trials')
   animal_ID = raw_input("Enter animal I.D: ")

   args = vars(ap.parse_args())
   #delay = float(args['delay'])
   limitTrial = float(args['limitTrial'])
   taskname = args['task']
   mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos = (0,0))

   run(taskname, mywin,limitTrial, animal_ID) #removed delay param



