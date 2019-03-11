from psychopy import visual, core, logging, event
import time, random, datetime
import marmocontrol as control
import pandas as pd
from reports import Report
from heatmap import scatterplot
import numpy as np
import math


def execTask(taskname,limitTrial,mywin, animal_ID,session):

    mouse = event.Mouse(win=mywin)
   

    #generating report directory
    results_col = ['Session','Timestamp','Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Reward Stimulus Position','Distance from reward center (px)', 'Fixation latency (s)', 'Response latency (ms)', 'Outsides', 'Success (Y/N)', 'Counter']
    summary_col = ['Session','Finished Session Time', 'Total Time', 'Trials', 'Hits', 'Misses', 'Timeouts', 'Outsides', 'Accuracy (%)', 'Average dist from center (Px)', 'Average response latency (s)', 'Reward Stimulus - Red', 'Success%']
    reportObj_trial = Report(str(taskname),animal_ID,results_col,'raw_data')
    reportObj_summary = Report(str(taskname), animal_ID, summary_col,'summary_data')
    reportObj_summary.createdir()
    reportObj_trial.createdir()
    results = []
    summary = []

    #setting initial parameters

    #dummy trial counter and trial limits
    trial = 1
    timeouts = 0
    outsides = 0
    total_outsides = 0
    timer = time.time()

    #dummy mouse position
    xpos = 0
    ypos = 0
    correct = []
    wrong = []

    hits = 0 #hit counter dummy
    stim_size = 250 #3cm equivalent on screen
    reaction_threshold = 2 # 2s threshold for selecting a choice before fixation cue is refreshed

    #set box positions

    left_box_coord = [-1280/4, 0]
    right_box_coord = [1280/4, 0]


    #set reward parameters, reward stimuli / variable = image

    reward_image = 'images/composite1-1.jpg'
    penalty_image = 'images/composite1-2.jpg'

    #pseudo-rng
    #if not wholly divisble by 2, will round to nearest integer.
    choice = np.repeat([0,1],math.floor(limitTrial/2))

    if math.floor(limitTrial%2) >0:
        choice = np.append(choice,random.randint(0,1))
    
    print(choice)
    np.random.shuffle(choice)
    print(choice)

    while trial <= limitTrial:
        for rand_stim in choice:
            t = time.time()  # returns time in sec as float

            # creating fixation cue
            fixation_cue = visual.GratingStim(win = mywin, size = stim_size, pos = (0,0), color = [-1,-1,-1], colorSpace = 'rgb', sf = 0)
            fixation_cue.draw(mywin)
            mywin.update()

            fixation_start = datetime.datetime.now()
            mouse.clickReset()
            checking1 = False
    
            while not checking1:
                while not mouse.getPressed()[0]:  # checks whether mouse button (i.e. button '0') was pressed
                    time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms
                if mouse.getPressed()[0] and mouse.isPressedIn(fixation_cue):
                    checking1 = True
                    fixation_end = datetime.datetime.now()
                    fixation_time = (fixation_end - fixation_start)
                else:
                    checking1 = False                    

            # creating left and right boxes

            left_mask = visual.GratingStim(win=mywin, size=stim_size, pos=left_box_coord, opacity = 0.0)
            right_mask = visual.GratingStim(win=mywin, size=stim_size, pos=right_box_coord, opacity = 0.0)

            if rand_stim == 0:
                left_image = reward_image
                reward_stim = left_mask
                reward_coord = left_box_coord
                penalty_coord = right_box_coord
                penalty_stim = right_mask
                right_image = penalty_image
                reward = 'left'
            elif rand_stim == 1:
                right_image = reward_image
                reward_stim = right_mask
                reward_coord = right_box_coord
                penalty_coord = left_box_coord
                penalty_stim = left_mask
                left_image = penalty_image
                reward = 'right'

            left_grating = visual.ImageStim(win=mywin, size=stim_size, pos=left_box_coord, image = left_image)
            right_grating = visual.ImageStim(win=mywin, size=stim_size, pos=right_box_coord, image = right_image)


            # drawing gratings
            reward_stim.draw(mywin)
            penalty_stim.draw(mywin)           
            right_grating.draw(mywin)
            left_grating.draw(mywin)

            mywin.update()

            print('Current reward position: ', reward)
            print('Current reward image: ', reward_image)
            reaction_start = datetime.datetime.now() # start reaction timer from drawing the grating

            # pre-loop dummies
            mouse.clickReset()  # resets a timer for timing button clicks
            checking2 = False
            timeout = False
            touch_timeout = True

            while not checking2:

                while not mouse.getPressed()[0] and not timeout:  # checks whether mouse button (i.e. button '0') was pressed
                    reaction_monitor = (datetime.datetime.now() - reaction_start).total_seconds()
                    touch_timeout = False
                    if reaction_monitor >= reaction_threshold:
                        timeout = True
                        checking2 = True
                        session_time = datetime.datetime.now().strftime("%H:%M %p")
                        append_array = [session, session_time, 'timeout', '', '', time.time() - t, reward,'', '> ' + str(reaction_threshold) + ' sec', '', outsides, 'N/A', '']
                        results.append(append_array)
                        #do not record as trial, reset number
                        
                        reportObj_trial.addEvent(results)

                        core.wait(1)
                        timeouts += 1
                        outsides = 0 #reset outside counter
                        print('Trial: ',trial)
                        
                        print(trial)
                        print(limitTrial)
                        
                    else:
                        time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms - THIS MUST BE ACCOUNTED FOR IF ACCURATELY TIMING RESPONSE LATENCIES

                if mouse.getPressed()[0] and not timeout:  # If pressed
                    xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
                    ypos = mouse.getPos()[1]

                    correct = mouse.isPressedIn(reward_stim) # Returns True if mouse pressed in grating
                    wrong = mouse.isPressedIn(penalty_stim)
                    reaction_end = datetime.datetime.now()

                    if correct is not True and wrong is not True and touch_timeout is not True: #if background pressed in
                        print('Current trial: ', trial)
                        print('Touch recorded outside grating')

                        dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                        session_time = datetime.datetime.now().strftime("%H:%M %p")
                        reaction_time = ((reaction_end - reaction_start).total_seconds())*1000
                        results.append([session, session_time, 'outside stimuli', xpos, ypos, time.time() - t, reward, dist_stim, fixation_time, reaction_time, '', 'N/A', ''])
                        #do not record as trial, reset number
                        reportObj_trial.addEvent(results)

                        outsides += 1
                        total_outsides += 1
                        print('Trial: ',trial)
                        touch_timeout = True          

                    elif correct == True:

                            mywin.flip()

                            #present reward stim for duration of reward
                            if rand_stim == 0:
                                left_grating.draw(mywin)
                            else:
                                right_grating.draw(mywin)                            

                            mywin.flip()                            
                            control.correctAnswer()

                            core.wait(0.5)  # stimulus presentation                       
                            
                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = ((reaction_end - reaction_start).total_seconds())*1000
                            results.append([session, session_time, trial, xpos, ypos, time.time() - t, reward, dist_stim, fixation_time, reaction_time, outsides, 'yes', 1])
                            hits += 1
                            trial += 1
                            outsides = 0 #reset outside counter

                            reportObj_trial.addEvent(results)

                            
                            mywin.flip()   

                            checking2 = True
                            
                            print(trial)
                            print(limitTrial)
                            

                    elif wrong == True:
                            
                        mywin.flip()
                            
                        #present penalty stim for initial duration of timeout
                        if rand_stim == 0:
                            right_grating.draw(mywin)
                        else:
                            left_grating.draw(mywin)
                            
                        mywin.flip()
                            
                        control.incorrectAnswer()

                        core.wait(0.5) #stimulus presentation
                            
                        dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                        session_time = datetime.datetime.now().strftime("%H:%M %p")
                        reaction_time = ((reaction_end - reaction_start).total_seconds())*1000
                        results.append([session,session_time,trial, xpos, ypos, time.time() - t, reward, dist_stim, fixation_time, reaction_time, outsides, 'no', 0])
                        reportObj_trial.addEvent(results)

                        mywin.flip()
                        trial += 1
                        outsides = 0 #reset outside counter
                        core.wait(2) #timeout

                        checking2 = True

                        print(trial)
                        print(limitTrial)


        ###########################################
    
    # Timer variables
    totalTime = time.time() - timer
    mins = int(totalTime / 60)
    secs = round((totalTime % 60), 1)
    timeLog = str(mins) + ' min ' + str(secs) + ' sec'
    
    # below, data presenting
    df_results = pd.DataFrame(results, columns=results_col)
    print(df_results)
    reportObj_trial.writecsv('trial', session)
    average_dist = float(df_results[['Distance from reward center (px)']].mean())
    avg_reactiontime = float(df_results[['Reaction time (s)']].mean())

    session_time = datetime.datetime.now().strftime("%H:%M %p")
    ## for reference ##  summary_col = ['Session','Finished Session Time', 'Total Time', 'Trials', 'Hits', 'Misses', 'Timeouts', 'Outsides', 'Accuracy (%)', 'Average dist from center (Px)', 'Average response latency (s)', 'Reward Stimulus - Red', 'Success%']
    summary.append([session, session_time, timeLog, limitTrial, hits, limitTrial - hits, timeouts, total_outsides, ((limitTrial+total_outsides)/limitTrial)*100, average_dist, avg_reactiontime, reward_image, (float(hits) / float(limitTrial)) * 100])
    sucess = (float(hits) / float(limitTrial)) * 100
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

    return totalTime, sucess