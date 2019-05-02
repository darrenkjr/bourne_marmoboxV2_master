#import classes from arduino control and from tasks - runs declared tasks, pre-import required modules + packages

import arduino_controlclass as control
from psychopy import visual, core, logging, event
import importlib

tasklist = ['tasks.drawframesRL']

#loading required tasks, and assigns each task a number
def loadtaskmodule(tasklist):
    taskmodule = []
    for x in tasklist:

        print(x)
        task = importlib.import_module(x)
        taskmodule.append(task)

        mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
        print('test')
        print(taskmodule)

        return taskmodule

taskmodule = loadtaskmodule(tasklist)

mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
taskmodule[0].run(mywin)