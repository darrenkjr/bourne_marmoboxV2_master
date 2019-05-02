#import classes from arduino control and from tasks - runs declared tasks, pre-import required modules + packages

import arduino_controlclass as control
from marmobox import tasklist
from psychopy import visual, core, logging, event

mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
print('test')

task = importlib.import_module()
task1.run(mywin)
