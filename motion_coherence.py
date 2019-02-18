from psychopy import visual, core, logging, event
import time, random, datetime
import marmocontrol as control
import pandas as pd
from reports import Report
from heatmap import scatterplot
import numpy as np
import math


# setting initial parameters
limitTrial = 5
mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
mouse = event.Mouse(win=mywin)

# dummy trial counter and trial limits
trial = 1
nulls = 0
timer = time.time()

# dummy mouse position
xpos = 0
ypos = 0
touchTimeout = False
correct = []
wrong = []

hits = 0  # hit counter dummy
stim_size = 200  # 3cm equivalent on screen

# set box positions
left_box_coord = [-1280 / 3, 0]
right_box_coord = [1280 / 3, 0]
centre_box = [0,0]

left_box = visual.GratingStim(win=mywin,size=stim_size,pos=left_box_coord, color = [-1,-1,1], colorSpace='rgb',sf=0)
right_box = visual.GratingStim(win=mywin,size=stim_size,pos=right_box_coord, color = [-1,-1,1], colorSpace='rgb',sf=0)

# pseudo-rng
# if not wholly divisble by 2, will round to nearest integer.
#0 = right, 1 = left
choice = np.repeat([0, 1], math.floor(limitTrial / 2))

if math.floor(limitTrial % 2) > 0:
    choice = np.append(choice, random.randint(0, 1))

print(choice)
np.random.shuffle(choice)
print(choice)

# in degrees
reward_dir = 0


dot_stim = visual.DotStim(win=mywin, units='', nDots=500, coherence=0.80, fieldPos=centre_box, fieldSize=(500,500),
                          fieldShape='sqr', dotSize=7, dotLife=200, dir=reward_dir, speed =5, opacity =1.0, contrast =1.0, signalDots='same', noiseDots='direction')

stop = False

if reward_dir == 0:
    reward_box = right_box
    incorrect_box = left_box

elif reward_dir == 180:
    reward_box = left_box
    incorrect_box = right_box

while stop == False:
    dot_stim.draw()
    left_box.draw()
    right_box.draw()
    mywin.update()

    if event.getKeys('q'):
        mywin.close()
        stop = True








