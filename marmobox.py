import marmocontrol as control
import argparse
import importlib
import time
from psychopy import visual
def run(taskname,delay):

   # detect marmoset
   mywin = visual.Window([1600,960], monitor="testMonitor", units="deg", pos = (0,0))
   mywin.flip()
   print 'Attempting to detect marmoset...'
   beamInput = True
   while beamInput:
       beamInput = control.readBeam()
   print 'Found! Now attempting to read RFID tag...'

   # read RFID tag
   # implement with rfid.py

   # launch experiment

   print 'Starting task: ' + str(taskname) + ' in ' + str(delay) + ' seconds...'

   time.sleep(float(delay))

   print 'Started!'

   task = importlib.import_module(taskname)
   mywin.close()
   results = task.execTask()

   print 'Done. These are the task results: \n'

   print 'trial,xpos,ypos,time,stimulus,reward'
   for r in results:
       print ','.join(str(c) for c in r)

    #if/elif statement which directs program to animal's csv. file (RFID dependent or otherwise)

 #  path = '/home/pi/marmobox/data/F1920.csv'
  # file = open(path, 'a') # + args['task'] + 
   #file.write('task, trial, xpos, ypos, stimulus, reward')
   #file.close()

if __name__ == '__main__':
   # initialise the argument parser
   ap = argparse.ArgumentParser()
   ap.add_argument('-t', '--task', help='name of the task')
   ap.add_argument('-d', '--delay', help='delay in seconds for executing tasks')
   args = vars(ap.parse_args())
   delay = float(args['delay'])
   task = args['task']
   run(task,delay)