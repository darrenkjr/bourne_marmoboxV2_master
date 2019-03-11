from psychopy import visual, core, logging, event
import time, random, datetime
import marmocontrol as control
from reports import Report
from heatmap import scatterplot
import pandas as pd

def execTask(taskname,limitTrial,mywin,animal_ID,session):

    #create window
    print('This is session:', session)
    mouse = event.Mouse(win=mywin)

    #generating report directories and objects
    results_col = ['Session','Timestamp', 'Trial', 'xpos', 'ypos', 'Time (s)', 'Stimuli color', 'Distance from stimulus center (Px)',
                   'Reaction time (s)', 'Success Y/N']
    summary_col = ['Session','Timestamp', 'Trials', 'Hits', 'Misses', 'Average distance from stimulus center (Px)',
                   'Avg reaction time (s)', 'Sucesss %']
    reportobj_trial = Report(str(taskname), animal_ID, results_col, 'raw_data')
    reportobj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
    reportobj_trial.createdir()
    reportobj_summary.createdir()
    results = []
    summary = []

    #create stimulus
    trial = 0
    buttons = []
    xpos = 0
    ypos = 0
    stimPosx = 0
    stimPosy = 0
    touchTimeout = False
    hits = 0
    size = 400
    timer = time.time()
    stimLimit = limitTrial // 3

    c1 = 0
    c2 = 0
    c3 = 0

    while trial < limitTrial:
        if c1 < stimLimit and c2 < stimLimit and c3 < stimLimit:
            y = random.randint(0,2)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            elif y == 1:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
            elif y == 2:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 < stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1				
        elif c1 < stimLimit and c2 == stimLimit and c3 < stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1
        elif c1 < stimLimit and c2 < stimLimit and c3 == stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
        elif c1 == stimLimit and c2 == stimLimit and c3 < stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb') 		
            x = 'yellow' 		
            c3 += 1
        elif c1 < stimLimit and c2 == stimLimit and c3 == stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
            x = 'blue' 		
            c1 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 == stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
            x = 'red' 		
            c2 += 1
        
        elif c1 == stimLimit and c2 == stimLimit and c3 == stimLimit: #if trial number is not divisible by three, select remainders at random
            y = random.randint(0,2)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
            elif y == 1:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
            elif y == 2:
                grating = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 
            
        trial = trial+1

        grating.draw()
        mywin.update()
        #starting reaction time recording after grating is drawn
        reaction_start = datetime.datetime.now()

        mouse.clickReset() #resets a timer for timing button clicks
        checking = False

        while not checking:
            while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed 
                touchTimeout = False
                time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
            else: #If pressed
                xpos = mouse.getPos()[0] #Returns current positions of mouse during press
                ypos = mouse.getPos()[1]
                buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating
                reaction_end = datetime.datetime.now()

            if buttons == True:
                if not touchTimeout:
                    control.correctAnswer()
                    dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
                    session_time = datetime.datetime.now().strftime("%d-%m-%y, %H:%M %p")
                    reaction_time = (reaction_end - reaction_start).total_seconds()
                    results.append([session,session_time,trial, xpos, ypos, round(time.time() - timer, 4), x, dist_stim,reaction_time, 'yes'])
                    reportobj_trial.addEvent(results)

                    touchTimeout = True
                    checking = True
                    hits += 1
                else:
                    time.sleep(0.01)
            else:
                if not touchTimeout:
                    control.incorrectAnswer()

                    dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
                    session_time = datetime.datetime.now().strftime("%d-%m-%y, %H:%M %p")
                    reaction_time = (reaction_end - reaction_start).total_seconds()

                    results.append([session,session_time,trial, xpos, ypos, round(time.time() - timer, 4), x, dist_stim,reaction_time, 'no'])
                    reportobj_trial.addEvent(results)

                    mywin.update()

                    core.wait(2) # specifies timeout period
                    touchTimeout = True
                    checking = True

        ###########################################
        # below, data presenting

    df_results = pd.DataFrame(results, columns=results_col)
    reportobj_trial.writecsv('trial', session)
    average_dist = float(df_results[['Distance from stimulus center (Px)']].mean())
    avg_reactiontime = float(df_results[['Reaction time (s)']].mean())

    session_time = datetime.datetime.now().strftime("%d-%m-%y, %H:%M %p")
    summary.append([session,session_time, limitTrial, hits, limitTrial - hits, average_dist, avg_reactiontime,
                    (float(hits) / float(limitTrial)) * 100])
    reportobj_summary.addEvent(summary)
    reportobj_summary.writecsv('summary', session)

    # organizing coordinates
    pressed = ([df_results['xpos']], [df_results['ypos']])
    stimulus = ([stimPosx
                 ], [stimPosy])
    # creating scatter object and saving heat map plot
    scatter = scatterplot(stimulus, pressed, size)
    scatter.heatmap_param(limitTrial, size)
    scatter.saveheatmap(taskname, animal_ID, limitTrial)

    totalTime = time.time() - timer
    sucess = (float(hits) / float(limitTrial)) * 100

    return totalTime, sucess
