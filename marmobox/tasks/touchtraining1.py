from psychopy import visual, core, logging, event
import time, datetime
import marmocontrol as control
from reports import Report
from heatmap import scatterplot
from tasks.helper.initialisation import initial_param
import pandas as pd


def run(taskname,limitTrial,mywin,animal_ID,session):
	# generating report directories and objects
	# results_col = ['Session','Timestamp','Trial', 'xpos', 'ypos', 'Time (s)', '-', 'Distance from stimulus center (Px)', 'Reaction time (s)', 'Success Y/N']
	# summary_col = ['Session','Session Time', 'Total Time (sec)', 'Trials','Hits','Misses', 'Average distance from stimulus center (Px)', 'Avg reaction time (s)', 'Success %']
	# reportobj_trial = Report(str(taskname), animal_ID, results_col, 'raw_data')
	# reportobj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
	# reportobj_trial.createdir()
	# reportobj_summary.createdir()
	# results = []
	# summary = []

	mouse, trial, nulls, timer, stimPosx, stimPoxy, touchTimeout, correct, wrong, hits, null, miss, results, summary = initial_param(mywin)


	stim_size = 700
	#create stimulus
	# limitTrial=3
	buttons = []
	xpos = 0
	stimPosx = 0
	stimPosy = 0
	ypos = 0
	hits = 0
	size = 700
	timer = time.time()
	centre_box = visual.GratingStim(win=mywin,size=stim_size,pos=[0,0], color = [-1,-1,1], colorSpace='rgb',sf=0)
	while trial < limitTrial:
		trial = trial+1
		t=time.time() #returns time in sec as float


		centre_box.draw()
		mywin.update()
		reaction_start = datetime.datetime.now()
		mouse.clickReset() #resets a timer for timing button clicks

		# start reaction timer from drawing the grating


		while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed
			time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
		else: #If pressed
			xpos = mouse.getPos()[0] #Returns current positions of mouse during press
			ypos = mouse.getPos()[1]
			buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating
			reaction_end = datetime.datetime.now()

		if buttons == True:
			control.correctAnswer()
			dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
			session_time = datetime.datetime.now().strftime("%H:%M %p")
			reaction_time = (reaction_end - reaction_start).total_seconds()
			results.append([session,session_time,trial, xpos, ypos, time.time() - t, '-', dist_stim, reaction_time, 'yes'])
			reportobj_trial.addEvent(results)
			hits += 1
		else:
			control.incorrectAnswer()
			dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2.0)
			session_time = datetime.datetime.now().strftime("%H:%M %p")
			reaction_time = (reaction_end - reaction_start).total_seconds()
			results.append([session,session_time,trial, xpos, ypos, time.time() - t, '-', dist_stim, reaction_time, 'no'])
			mywin.update()
			reportobj_trial.addEvent(results)
			core.wait(2) # specifies timeout period

	###########################################
	# below, data presenting

    	# Timer variables
	totalTime = time.time() - timer
	mins = int(totalTime / 60)
	secs = round((totalTime % 60), 1)
	timeLog = str(mins) + ' min ' + str(secs) + ' sec'

	df_results = pd.DataFrame(results, columns=results_col)
	reportobj_trial.writecsv('trial',session)
	average_dist = float(df_results[['Distance from stimulus center (Px)']].mean())
	avg_reactiontime = float(df_results[['Reaction time (s)']].mean())

	session_time = datetime.datetime.now().strftime("%H:%M %p")
	summary.append([session,session_time, timeLog, limitTrial, hits, limitTrial - hits, average_dist, avg_reactiontime, (float(hits) / float(limitTrial)) * 100])
	sucess = (float(hits) / float(limitTrial)) * 100
	reportobj_summary.addEvent(summary)
	reportobj_summary.writecsv('summary',session)

	#organizing coordinates
	pressed = ([df_results['xpos']], [df_results['ypos']])
	stimulus = ([stimPosx],[stimPosy])
	#creating scatter object and saving heat map plot
	scatter = scatterplot(stimulus,pressed,size)
	scatter.heatmap_param(limitTrial,size)
	scatter.saveheatmap(taskname,animal_ID,limitTrial)

	totalTime = time.time() - timer

	return totalTime, sucess
	
	
	
	
	
	


