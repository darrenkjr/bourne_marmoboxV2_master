from psychopy import visual, core, event
import time, datetime
from archive import marmocontrol as control
import pandas as pd
from archive.reports import Report
from archive.heatmap import scatterplot
import numpy as np

#reward color = yellow

def execTask(taskname,limitTrial,mywin, animal_ID,session):

    mouse = event.Mouse(win=mywin)

    #generating report directory
    results_col = ['Session','Timestamp','Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Reward Stimulus Position','Distance from reward center (px)', 'Reaction time (s)', 'Success (Y/N)']
    summary_col = ['Session','Finished Session Time','Trials', 'Hits', 'Misses', 'Average dist from center (Px)', 'Average reaction time (s)', 'Reward Stimulus - Red', 'Success%']
    reportObj_trial = Report(str(taskname),animal_ID,results_col,'raw_data')
    reportObj_summary = Report(str(taskname), animal_ID, summary_col,'summary_data')
    reportObj_summary.createdir()
    reportObj_trial.createdir()
    results = []
    summary = []

    #setting initial parameters

    #dummy trial counter and trial limits
    trial = 1
    timer = time.time()
    stimLimit = limitTrial // 3

    #dummy mouse position
    xpos = 0
    ypos = 0
    touchTimeout = False
    correct = []
    wrong = []

    hits = 0 #hit counter dummy
    stim_size = 250 #3cm equivalent on screen

    #set box positions

    left_box_coord = [-1280/4, 0]
    right_box_coord = [1280/4, 0]


    #set reward parameters, reward stimuli / variable = face
    yellow = [1,1,-1]
    red = [1,-1,-1]

    reward_face = 'circle'
    penalty_face = 'cross'

    left_face = 'circle'
    right_face = 'cross'



    #pseudo-rng
    #if not wholly divisble by 2, will round to nearest integer.
    choice = np.repeat([0,1],limitTrial/2)
    print(choice)
    np.random.shuffle(choice)
    print(choice)

    while trial < limitTrial:
        for rand_stim in choice:
            t = time.time()  # returns time in sec as float

            # creating left and right boxes

            left_grating = visual.GratingStim(win=mywin, size=stim_size, pos=left_box_coord, sf=20/stim_size, mask = left_face)
            right_grating = visual.GratingStim(win=mywin, size=stim_size, pos=right_box_coord, sf=20/stim_size, mask = right_face)

            if rand_stim == 0:
                reward_stim = left_grating
                reward_coord = left_box_coord
                penalty_coord = right_box_coord
                penalty_stim = right_grating
                left_face = reward_face
                right_face = penalty_face
                reward = 'left'
            elif rand_stim == 1:

                reward_stim = right_grating
                reward_coord = right_box_coord
                penalty_coord = left_box_coord
                penalty_stim = left_grating
                left_face = penalty_face
                right_face = reward_face
                reward = 'right'

            left_grating = visual.GratingStim(win=mywin, size=stim_size, pos=left_box_coord, sf=10 / 80, mask=left_face)
            right_grating = visual.GratingStim(win=mywin, size=stim_size, pos=right_box_coord, sf=20 / 80,
                                               mask=right_face)

            # drawing gratings
            right_grating.draw(mywin)
            left_grating.draw(mywin)

            mywin.update()

            print('Current reward position: ', reward)
            print('Current reward face', reward_face)
            reaction_start = datetime.datetime.now()
            # start reaction timer from drawing the grating

            mouse.clickReset()  # resets a timer for timing button clicks
            checking = False

            while not checking:
                while not mouse.getPressed()[0]:  # checks whether mouse button (i.e. button '0') was pressed
                    touchTimeout = False
                    time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms
                else:  # If pressed
                    xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
                    ypos = mouse.getPos()[1]

                    correct = mouse.isPressedIn(reward_stim) # Returns True if mouse pressed in grating
                    wrong = mouse.isPressedIn(penalty_stim)
                    reaction_end = datetime.datetime.now()

                    if correct is not True and wrong is not True:
                        print('Current trial: ', trial)
                        if not touchTimeout:

                            print('Touch recorded outside grating')

                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = (reaction_end - reaction_start).total_seconds()
                            results.append([session, session_time, 'outside stimuli', xpos, ypos, time.time() - t, reward, dist_stim, reaction_time, 'N/A'])
                            #do not record as trial, reset number
                            reportObj_trial.addEvent(results)

                            core.wait(1)
                            print('Trial: ',trial)


                    elif correct == True:
                        if not touchTimeout:
                            control.correctAnswer()
                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = (reaction_end - reaction_start).total_seconds()
                            results.append([session, session_time, trial, xpos, ypos, time.time() - t, reward, dist_stim, reaction_time, 'yes'])


                            reportObj_trial.addEvent(results)
                            hits += 1

                            trial += 1

                            checking = True

                        else:
                            time.sleep(0.01)

                    elif wrong == True:
                        if not touchTimeout:
                            control.incorrectAnswer()


                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = (reaction_end - reaction_start).total_seconds()


                            results.append([session,session_time,trial, xpos, ypos, time.time() - t, reward, dist_stim, reaction_time, 'no'])
                            reportObj_trial.addEvent(results)
                            mywin.update()

                            trial += 1
                            core.wait(2)

                            checking = True





        ###########################################
    # below, data presenting

    df_results = pd.DataFrame(results, columns=results_col)
    print(df_results)
    reportObj_trial.writecsv('trial', session)
    average_dist = float(df_results[['Distance from reward center (px)']].mean())
    avg_reactiontime = float(df_results[['Reaction time (s)']].mean())

    session_time = datetime.datetime.now().strftime("%H:%M %p")
    summary.append([session, session_time, limitTrial, hits, limitTrial - hits, average_dist, avg_reactiontime, reward_face,
                    (float(hits) / float(limitTrial)) * 100])
    reportObj_summary.addEvent(summary)
    reportObj_summary.writecsv('summary', session)

    # organizing coordinates
    pressed = ([df_results['X-Position (Pressed)']], [df_results['Y-Position (Pressed)']])
    print(reward_coord)
    stimulus = ([reward_coord[0], penalty_coord[0]], [reward_coord[1], penalty_coord[1]])
    # creating scatter object and saving heat map plot
    scatter = scatterplot(stimulus, pressed, stim_size)
    scatter.heatmap_param(limitTrial, stim_size)
    scatter.saveheatmap(taskname, animal_ID, limitTrial)

    totalTime = time.time() - timer

    return totalTime






