from psychopy import visual, event
import datetime
from tasks.helper.initialisation import initial_param
from tasks.helper.fixation import fixation

def run(mywin):
    #setting initial parameters
    limitTrial = 5
    mouse = event.Mouse(win=mywin)

    # setting initial parameters
    mouse,trial,nulls,timer,xpos,ypos, touchTimeout,correct,wrong,hits,null, miss, results, summary = initial_param(mywin)
    stim_size = 250  # 3cm equivalent on screen
    taskname = 'draw_frameRL'

    imagelist = ['tasks/images/composite1-1.jpg','tasks/images/composite1-2.jpg','tasks/images/composite2-1.jpg', 'tasks/images/composite2-2.jpg','tasks/images/composite3-2.jpg', 'tasks/images/composite3-1.jpg','tasks/images/composite4-1.jpg','tasks/images/composite4-2.jpg']
    primer_frames = 100


    while trial <= limitTrial:
        reaction_threshold = 2
        fixate_obj = fixation(mywin, taskname, stim_size, mouse, trial, reaction_threshold)
        fixation_time = fixate_obj.time_to_fixate

        counter = 0
        time_start = datetime.datetime.now()
        for frame in range(primer_frames):
            test_im1 = visual.ImageStim(win=mywin, size=stim_size, pos=[-1280 / 4, 0], image=imagelist[counter])
            # test_im = visual.ImageStim(win=mywin, size=stim_size, pos=[-1280 / 4, 0], image=imagelist[counter])
            test_im2 = visual.ImageStim(win=mywin, size=stim_size, pos=[1280 / 4, 0], image=imagelist[-counter])
            left_mask = visual.GratingStim(win=mywin, size=stim_size, pos=[-1280 / 4, 0], opacity=0.0)
            right_mask = visual.GratingStim(win=mywin, size=stim_size, pos=[1280 / 4, 0], opacity=0.0)

            test_im = visual.ImageStim(win=mywin, size=stim_size, pos=[-1280 / 4, 0], image=imagelist[counter])
            test_im1.draw()
            test_im2.draw()
            mywin.flip()

            counter += 1

            if counter > 7:
                counter = 0

        time_delta = (datetime.datetime.now() - time_start).total_seconds()
        print('Time taken to draw 100 frames', time_delta)
        trial += 1



