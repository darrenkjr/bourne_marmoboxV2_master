from psychopy import visual, core, logging, event
import time, datetime
import pandas as pd
from reports import Report
from heatmap import scatterplot
from initialisation import fixation, initial_param, rng_choice
from touchresults import motion_coherence_results

# setting initial parameters
limitTrial = 5
mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
mouse = event.Mouse(win=mywin)

# setting initial parameters
mouse,trial,nulls,timer,xpos,ypos, touchTimeout,correct,wrong,hits,null, miss, results, summary = initial_param(mywin)
stim_size = 200  # 3cm equivalent on screen
taskname = 'motioncoherence_LRdir'

#pseudo-rng determining direction of motion coherence dots
possible_selection = 2
choice = rng_choice(possible_selection,limitTrial)

# set box positions
left_box_coord = [-1280 / 2.5, 0]
right_box_coord = [1280 / 2.5, 0]

left_box = visual.GratingStim(win=mywin,size=stim_size,pos=left_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)
right_box = visual.GratingStim(win=mywin,size=stim_size,pos=right_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)

#pseudo-rng determining direction of motion coherence dots.
choice = rng_choice(possible_selection, limitTrial)

#in degrees
reward_dir = 0
stop = False
while trial <= limitTrial:
    #begin sampling from RNG, 0 = right, 1 = left
    for dir in choice:
        if dir == 0:
            reward_stim = right_box
            penalty_stim = left_box
            reward_dir = 0

        else:
            reward_stim = left_box
            penalty_stim = right_box
            reward_dir = 180.0

        time_to_fixate = fixation(mywin, taskname, stim_size,mouse,trial)

        #display dot_stim for 100 frames first, then display left and right boxes
        primer_frames = 100
        dot_stim = visual.DotStim(win=mywin, units='', nDots=500, coherence=1, fieldPos=(0,0), fieldSize=(600, 600),
                                  fieldShape='circle', dotSize=10, dotLife=100, dir=reward_dir, speed=5, opacity=1.0,
                                  contrast=1.0, signalDots='same', noiseDots='direction')

        for frames in range(primer_frames):

            dot_stim.draw()
            mywin.flip()

        print('presenting options')
        stop = False
        mywin.flip()

        #now draw stimuli
        while stop == False:
            mouse.clickReset()
            checking = False

            while not checking:
                while not mouse.getPressed()[0]:
                    touchTimeout = False
                    dot_stim.draw()
                    left_box.draw()
                    right_box.draw()
                    mywin.flip()

                else:  # If pressed
                    xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
                    ypos = mouse.getPos()[1]

                    correct = mouse.isPressedIn(reward_stim)  # Returns True if mouse pressed in grating
                    incorrect = mouse.isPressedIn(penalty_stim)
                    #begin touch detection and handling of results
                    nulls, miss, trial, hits = motion_coherence_results(checking,stop,correct,incorrect,touchTimeout,nulls,trial,miss,hits,mywin)


            if event.getKeys('q'):
                mywin.close()
                stop = True
