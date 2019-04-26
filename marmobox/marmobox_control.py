#import classes from arduino control and from tasks - runs declared tasks, pre-import required modules + packages

import arduino_controlclass as control
import tasks.draw_framesRL as test
from psychopy import visual, core, logging, event

mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
taskname = 'draw_framesRL'

test