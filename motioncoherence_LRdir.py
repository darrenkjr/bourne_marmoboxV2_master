from psychopy import visual, core, logging, event
import time, random, datetime
import marmocontrol as control
import pandas as pd
from reports import Report
from heatmap import scatterplot
import numpy as np
import math
from fixation import fixation

#temporary paramters delete when integrating into thebadtouch
taskname = 'motioncoherence_LRdir'
animal_ID = 'test'
session = 0
limitTrial = 5

# setting initial parameters

mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
mouse = event.Mouse(win=mywin)
coherence = 0.9

#setting report parameters
results_col = ['Session', 'Timestamp', 'Trial', 'Time to fixate (s)', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Reward Stimulus Position', 'Distance from reward center (px)', 'Reaction time (s)', 'Success (Y/N)']
summary_col = ['Session','Finished Session Time', 'Coherence', 'Total Time', 'Trials', 'Hits', 'Misses', 'Nulls', 'Average dist from center (Px)', 'Average reaction time (s)', 'Average time to fixate (s)', 'Success%']

reportObj_trial = Report(str(taskname),animal_ID,results_col,'raw_data')

# generating report directory

reportObj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
reportObj_summary.createdir()
reportObj_trial.createdir()
results = []
summary = []

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
null = 0
miss = 0
stim_size = 200  # 3cm equivalent on screen

# set box positions
left_box_coord = [-1280 / 2.5, 0]
right_box_coord = [1280 / 2.5, 0]


left_box = visual.GratingStim(win=mywin,size=stim_size,pos=left_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)
right_box = visual.GratingStim(win=mywin,size=stim_size,pos=right_box_coord, color = [1,1,1], colorSpace='rgb',sf=0)

# pseudo-rng determining direction of motion coherence dots.
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

stop = False
while trial <= limitTrial:
    # testing central fixation
    for dir in choice:
        if dir == 0:
            reward_box = right_box
            reward_coord = right_box_coord
            reward = 'right'
            incorrect_box = left_box
            penalty_coord = left_box_coord
            reward_dir = 0

        else:
            reward_box = left_box
            reward_coord = left_box_coord
            reward = 'left'
            incorrect_box = right_box
            penalty_coord = right_box_coord
            reward_dir = 180.0

        #first check fixation
        time_to_fixate = fixation(mywin, taskname, stim_size, mouse, trial)

        #display dot_stim for 100 frames first, then display left and right boxes
        primer_frames = 100
        dot_stim = visual.DotStim(win=mywin, units='', nDots=500, coherence=coherence, fieldPos=(0,0),
                                  fieldSize=(600, 600),
                                  fieldShape='circle', dotSize=10, dotLife=50, dir=reward_dir, speed=5, opacity=1.0,
                                  contrast=1.0, signalDots='same', noiseDots='direction')

        for frames in range(primer_frames):

            dot_stim.draw()
            mywin.flip()

        print('presenting options')
        stop = False
        mywin.flip()
        reaction_start = datetime.datetime.now()

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
                    t = time.time()

                else:  # If pressed
                    xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
                    ypos = mouse.getPos()[1]

                    correct = mouse.isPressedIn(reward_box)  # Returns True if mouse pressed in grating
                    incorrect = mouse.isPressedIn(incorrect_box)
                    reaction_end = datetime.datetime.now()

                    #count nulls.
                    if correct is not True and incorrect is not True:
                        print('Current trial: ', trial)
                        if not touchTimeout:

                            print('Touch recorded outside grating')
                            nulls += 1
                            print('Trial: ',trial)

                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = reaction_time = (reaction_end - reaction_start).total_seconds()

                            results.append(
                                [session, session_time, 'outside stimuli', time_to_fixate, xpos, ypos, time.time() - t, reward,
                                 dist_stim,
                                 reaction_time, 'null'])

                            reportObj_trial.addEvent(results)

                    elif correct == True:
                        if not touchTimeout:
                            print('Hit!')
                            hits += 1
                            trial += 1

                            control.correctAnswer()
                            mywin.flip()
                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = reaction_time = (reaction_end - reaction_start).total_seconds()

                            results.append(
                                [session, session_time, trial, time_to_fixate, xpos, ypos, time.time() - t, reward, dist_stim,
                                 reaction_time, 'yes'])

                            reportObj_trial.addEvent(results)

                            core.wait(0.5)
                            checking = True
                            stop = True

                        else:
                            time.sleep(0.01)

                    elif incorrect == True:
                        if not touchTimeout:
                            print('Miss!')
                            miss +=1
                            trial += 1

                            control.incorrectAnswer()
                            mywin.flip()

                            dist_stim = ((reward_coord[0] - xpos) ** 2 + (reward_coord[1] - ypos) ** 2) ** (1 / 2.0)
                            session_time = datetime.datetime.now().strftime("%H:%M %p")
                            reaction_time = reaction_time = (reaction_end - reaction_start).total_seconds()

                            results.append(
                                [session, session_time, trial, time_to_fixate, xpos, ypos, time.time() - t, reward,
                                 dist_stim,
                                 reaction_time, 'no'])

                            reportObj_trial.addEvent(results)

                            core.wait(2.0)
                            checking = True
                            stop = True

                        else:
                            time.sleep(0.01)



        if event.getKeys('q'):
            mywin.close()
            stop = True

# Timer variables
totalTime = time.time() - timer
mins = int(totalTime / 60)
secs = round((totalTime % 60), 1)
timeLog = str(mins) + ' min ' + str(secs) + ' sec'

# below, data presenting
df_results = pd.DataFrame(results, columns=results_col)
reportObj_trial.writecsv('trial', session)
average_dist = float(df_results[['Distance from reward center (px)']].mean())
avg_reactiontime = float(df_results[['Reaction time (s)']].mean())
avg_timetofixate = float(df_results[['Time to fixate (s)']].mean())

session_time = datetime.datetime.now().strftime("%H:%M %p")
summary.append(
    [session, session_time, coherence, timeLog, limitTrial, hits, limitTrial - hits, nulls, average_dist, avg_reactiontime, avg_timetofixate,
     (float(hits) / float(limitTrial)) * 100])

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
