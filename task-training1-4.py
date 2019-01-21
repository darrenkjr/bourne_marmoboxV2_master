from psychopy import visual, core, logging, event
import time, random, datetime
import marmocontrol as control
import pandas as pd
from reports import Report
from heatmap import scatterplot
import numpy as np

def execTask(taskname,limitTrial,mywin, animal_ID):

    mouse = event.Mouse(win=mywin)

    #generating report directory
    results_col = ['Timestamp','Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Stimulus type','Stimulus Position (Center)','Distance from center (px)', 'Reaction time', 'Success (Y/N)']
    summary_col = ['Finished Session Time','Minutes','Seconds', 'Trials', 'Hits', 'Misses', 'Average dist from center (Px)', 'Average reaction time (s)', 'Success%']
    reportObj_trial = Report(str(taskname),animal_ID,results_col,'raw_data')
    reportObj_summary = Report(str(taskname), animal_ID, summary_col,'summary_data')
    reportObj_summary.createdir()
    reportObj_trial.createdir()
    results = []
    summary = []

    #setting initial parameters
    trial = 0
    xpos = 0
    ypos = 0
    touchTimeout = False
    hits = 0
    stim_size = 250
    x = 0
    printPos = 0
    reward = 0
    stimx = []
    stimy = []
    stim_coord = []
    session = 1
    rangex = 1280/2 - stim_size/2
    rangey = 720/2 - stim_size/2 

    #set stimuli limit and trial counter variables
    stimLimit = limitTrial // 3
    c1 = 0
    c2 = 0
    c3 = 0

    timer = time.time()
    #display colours and position in pseudorandom sequence
    while trial < limitTrial:

        #create stimuli
        stimPosx = random.uniform(-rangex,rangex)
        stimPosy = random.uniform(-rangey,rangey)
        blue = visual.GratingStim(win=mywin, size=stim_size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb')
        red = visual.GratingStim(win=mywin, size=stim_size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb')
        yellow = visual.GratingStim(win=mywin, size=stim_size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb')
        #mask = visual.GratingStim(win=mywin, size = stim_size*1.5, pos=[stimPosx,stimPosy], opacity = 0.0)

        if c1 < stimLimit and c2 < stimLimit and c3 < stimLimit:
            a = random.randint(0,2)
            if a == 0:
                grating = blue
                x = 'blue'
                c1 += 1
            elif a == 1:
                grating = red
                x = 'red'
                c2 += 1
            elif a == 2:
                grating = yellow
                x = 'yellow'
                c3 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 < stimLimit:
            a = random.randint(0,1)
            if a == 0:
                grating = red
                x = 'red'
                c2 += 1
            else:
                grating = yellow
                x = 'yellow'
                c3 += 1
        elif c1 < stimLimit and c2 == stimLimit and c3 < stimLimit:
            a = random.randint(0,1)
            if a == 0:
                grating = blue
                x = 'blue'
                c1 += 1
            else:
                grating = yellow
                x = 'yellow'
                c3 += 1
        elif c1 < stimLimit and c2 < stimLimit and c3 == stimLimit:
            a = random.randint(0,1)
            if a == 0:
                grating = blue
                x = 'blue'
                c1 += 1
            else:
                grating = red
                x = 'red'
                c2 += 1
        elif c1 == stimLimit and c2 == stimLimit and c3 < stimLimit:
            grating = yellow
            x = 'yellow'
            c3 += 1
        elif c1 < stimLimit and c2 == stimLimit and c3 == stimLimit:
            grating = blue
            x = 'blue'
            c1 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 == stimLimit:
            grating = red
            x = 'red'
            c2 += 1
        elif c1 == stimLimit and c2 == stimLimit and c3 == stimLimit: #if trial number is not divisible by three, select remainders at random
            y = random.randint(0,2)
            if y == 0:
                grating = blue
                x = 'blue'
            elif y == 1:
                grating = red
                x = 'red'
            elif y == 2:
                grating = yellow
                x = 'yellow'

        trial = trial+1

        #mask.draw()
        grating.draw()
        mywin.update()
        mouse.clickReset() #resets a timer for timing button clicks
        checking = False

        #start reaction timer from drawing the grating
        reaction_start = datetime.datetime.now()

        while not checking:
            while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed
                touchTimeout = False
                time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
            else: #If pressed
                xpos = mouse.getPos()[0] #Returns current positions of mouse during press
                ypos = mouse.getPos()[1]
                buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in mask
                reaction_end = datetime.datetime.now()

            if buttons == True:
                if not touchTimeout:
                    control.correctAnswer()

                    #calculating center position of stimulus and distance of touch fromm stimuli center
                    printPos = str(stimPosx) + ',' + str(stimPosy)
                    stimx.append(stimPosx)
                    stimy.append(stimPosy)
                    session_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M %p")

                    reaction_time = (reaction_end - reaction_start).total_seconds()

                    dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
                    results.append([session_time,trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, dist_stim, reaction_time, 'yes'])
                    reportObj_trial.addEvent(results)
                    touchTimeout = True
                    checking = True
                    hits += 1
                    print('Reaction time (s): ', str(reaction_time))
                else:
                    time.sleep(0.01)

            else:
                if not touchTimeout:
                    control.incorrectAnswer()
                    printPos = str(stimPosx) + ',' + str(stimPosy)
                    stimx.append(stimPosx)
                    stimy.append(stimPosy)
                    dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
                    session_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M %p")

                    reaction_time = (reaction_end - reaction_start).total_seconds()

                    results.append([session_time, trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, dist_stim, reaction_time, 'no'])
                    reportObj_trial.addEvent(results)
                    mywin.update()
                    core.wait(5) # specifies trial delay in seconds
                    touchTimeout = True
                    checking = True

            df_results = pd.DataFrame(results, columns = results_col)

            #taking pressed data and stimulus data
            pressed = ([df_results['X-Position (Pressed)']], [df_results['Y-Position (Pressed)']])

    totalTime = time.time() - timer
    average_dist = float(df_results[['Distance from center (px)']].mean())
    average_rtime = float(df_results[['Reaction time']].mean())
    mins = int(totalTime / 60)
    secs = round((totalTime % 60), 1)
    fin_session_time = datetime.datetime.now().strftime("%H:%M %p")
    summary.append([fin_session_time,mins,secs, limitTrial,hits, (limitTrial - hits), average_dist, average_rtime, float(hits)/float(limitTrial)*100])
    reportObj_summary.addEvent(summary)

    #writing csv
    reportObj_summary.writecsv('summary',session)
    reportObj_trial.writecsv('trial',session)

    # creating heatmap plots and saving
    # to ensure translaton back to 'center', stimx and stimy gives info on amount of translation needed to provide the same result
    #hence set stimulus = [0,0] and subtract all elements within pressed coordinates by provided translation
    #converting to matrix
    mat_stim = np.array([stimx,stimy])
    pressed_translated = [(np.array(pressed[0]) - mat_stim[0]), (np.array(pressed[1]) - mat_stim[1])]
    stimulus = mat_stim - mat_stim

    scatter = scatterplot(stimulus, pressed_translated, stim_size)
    scatter.heatmap_param(limitTrial,stim_size)
    scatter.saveheatmap(taskname, animal_ID,limitTrial)
    return totalTime



