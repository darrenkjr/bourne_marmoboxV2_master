from psychopy import visual, core, logging, event
import time, random, datetime, math
import numpy as np



def fixation(mywin, taskname, stim_size,mouse,trial):
    fix_coord = [0, 0]
    centre_box = visual.GratingStim(win=mywin, size=stim_size, pos= fix_coord, color=[-1, -1, -1],
                                    colorSpace='rgb', sf=0)

    print('checking central fixation')

    centre_box.draw()
    mywin.flip()

    mouse.clickReset()
    fix_start = datetime.datetime.now()

    fixation = False
    print('starting')

    while fixation == False:
        while not mouse.getPressed()[0]:  # checks whether mouse button (i.e. button '0') was pressed
            touchTimeout = False
            time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms
        else:  # If pressed
            xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
            ypos = mouse.getPos()[1]
            fixate_button = mouse.isPressedIn(centre_box)

            if fixate_button == True:
                if not touchTimeout:
                    print('Hit!')
                    time_to_fixate = (datetime.datetime.now() - fix_start).total_seconds()
                    print('Time to fixate (s): ', time_to_fixate)

                    trial += 1

                    mywin.flip()
                    touchTimeout = True
                    fixation = True

                else:
                    time.sleep(0.01)

            if not fixate_button:
                time.sleep(0.01)

    return time_to_fixate

def initial_param(mywin):
    mouse = event.Mouse(win=mywin)
    trial = 1
    nulls = 0
    timer = time.time()
    xpos = 0
    ypos = 0
    touchTimeout = False
    correct = []
    wrong = []
    hits = 0
    null = 0
    miss = 0
    results = []
    summary = []

    return mouse, trial,nulls,timer,xpos,ypos, touchTimeout,correct,wrong,hits,null, miss, results, summary

def rng_choice(possible_selection,limitTrial):

    choice = np.repeat([0, possible_selection -1], math.floor(limitTrial / 2))
    if math.floor(limitTrial % 2) > 0:
        choice = np.append(choice, random.randint(0, 1))
    np.random.shuffle(choice)

    return choice



