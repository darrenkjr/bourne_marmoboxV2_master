#import classes from arduino control and from tasks - runs declared tasks, pre-import required modules + packages

import arduino_controlclass as control
from psychopy import visual, core, logging, event
import importlib

tasklist = ['tasks.drawframesRL']

for x in tasklist:
    print(x)
    task1 = importlib.import_module(x)
    # import tasks.touchtraining1 as task2

    mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
    print('test')

    task1.run(mywin)
