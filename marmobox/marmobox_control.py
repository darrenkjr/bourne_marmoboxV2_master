#import classes from arduino control and from tasks - runs declared tasks, pre-import required modules + packages

import arduinocontrol as control
from psychopy import visual
import importlib

tasklist = ['tasks.drawframesRL','tasks.motioncoherenceLRdir']

#or load in required tasklist from json

#loading required tasks, and assigns each task a number
def loadtaskmodule(tasklist):
    taskmodule = []
    for x in tasklist:

        print(x)
        task = importlib.import_module(x)
        taskmodule.append(task)

        print('test')
        print(taskmodule)

    return taskmodule

taskmodule = loadtaskmodule(tasklist)

mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
taskmodule[0].run(mywin)



