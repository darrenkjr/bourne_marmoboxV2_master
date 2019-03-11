from psychopy import visual, core, logging, event
import time, datetime
import marmocontrol as control
import pandas as pd
from reports import Report
from heatmap import scatterplot
from initialisation import fixation, initial_param, rng_choice

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
centre_box_coord = [0,0]

left_box = visual.GratingStim(win=mywin,size=stim_size,pos=left_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)
right_box = visual.GratingStim(win=mywin,size=stim_size,pos=right_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)
centre_box = visual.GratingStim(win=mywin,size=stim_size,pos=centre_box_coord, color = [-1,-1,-1], colorSpace='rgb',sf=0)


# pseudo-rng determining direction of motion coherence dots.
# if not wholly divisble by 2, will round to nearest integer.
#0 = right, 1 = left
choice = rng_choice(possible_selection, limitTrial)

# in degrees
reward_dir = 0
stop = False
while trial <= limitTrial:
    #begin sampling from RNG, 0 = right, 1 = left
    for dir in choice:
        if dir == 0:
            reward_box = right_box
            incorrect_box = left_box
            reward_dir = 0

        else:
            reward_box = left_box
            incorrect_box = right_box
            reward_dir = 180.0

        time_to_fixate = fixation(mywin, taskname, stim_size,mouse,trial)

        #display dot_stim for 100 frames first, then display left and right boxes
        primer_frames = 100
        dot_stim = visual.DotStim(win=mywin, units='', nDots=500, coherence=1, fieldPos=centre_box_coord, fieldSize=(600, 600),
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

                    correct = mouse.isPressedIn(reward_box)  # Returns True if mouse pressed in grating
                    incorrect = mouse.isPressedIn(incorrect_box)

                    #count nulls.
                    if correct is not True and incorrect is not True:
                        print('Current trial: ', trial)
                        if not touchTimeout:

                            print('Touch recorded outside grating')
                            core.wait(1)
                            nulls += 1
                            print('Trial: ', trial)

                    elif incorrect == True:
                        if not touchTimeout:
                            print('Miss!')
                            miss +=1
                            trial += 1

                            mywin.flip()
                            core.wait(2.0)
                            checking = True
                            stop = True

                        else:
                            time.sleep(0.01)

                    elif correct == True:
                        if not touchTimeout:
                            print('Hit!')
                            hits += 1
                            trial +=1

                            mywin.flip()
                            core.wait(0.1)
                            checking = True
                            stop = True

                        else:
                            time.sleep(0.01)

                        if event.getKeys('q'):
                            mywin.close()
                            stop = True
