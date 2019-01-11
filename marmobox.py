import marmocontrol as control
import argparse
import importlib
import time, datetime
from psychopy import visual, core, logging, event
import pandas as pd
import os

#to run, in terminal - python marmobox.py -t -taskname -d -delay amt in no. -l -amount of trials required

def run(taskname,delay, limitTrial, mywin):
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
   print('Starting task: ' + str(taskname) + ' in ' + str(delay) + ' seconds...')

   time.sleep(float(delay))

   print('Started!')

   task = importlib.import_module(taskname)
#    mywin.close()
   results, summary = task.execTask(mywin, limitTrial, animal_ID)
   #note that summary is being returned as a dictionary data structure
    
   print('Detailed Results: \n')

   print('Trial, Touch Position (x,y), Time (sec), Stimulus (task-specific), Reward:')

   for r in results:
       print(','.join(str(c) for c in r))
   print('\n')

   # singular trial report generation

   results_col = ['trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Stimulus type',
                  'Stimulus Position (Center)', 'Success (Y/N)']
   df = pd.DataFrame(results, columns=results_col)
   dir_path = r'C:\Users\darre\PycharmProjects\BOURNE_MARMOBOX\data'
   df.to_csv(os.path.join(dir_path, animal_ID + taskname + '_' + r'_trial_results.csv'), mode='a')

   print('Summary Results: \n')

   #summary result report generation
   df_summary = pd.Series(summary).to_frame()
   df_summary = df_summary.transpose()
   df_summary.set_index('Timestamp')
   print(df_summary)
   df_summary.to_csv(os.path.join(dir_path, animal_ID + taskname + '_' + r'_summary_results.csv'), mode='a', header = None)



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
   ap.add_argument('-l', '--limitTrial', help = 'input number of required trials')
   animal_ID = str(input("Enter animal I.D: "))

   args = vars(ap.parse_args())
   delay = float(args['delay'])
   limitTrial = float(args['limitTrial'])
   task = args['task']
   mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos = (0,0))

   run(task,delay,limitTrial,mywin)

