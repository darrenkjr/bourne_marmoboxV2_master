from psychopy import visual, core, logging, event
import time, datetime
import marmocontrol as control
from reports import Report
from heatmap import scatterplot
import pandas as pd


def execTask(taskname,limitTrial,mywin,animal_ID,session):
	mouse = event.Mouse(win=mywin)

	# generating report directories and objects
	results_col = ['Session','Timestamp','Trial', 'xpos', 'ypos', 'Time (s)', '-', 'Distance from stimulus center (Px)', 'Reaction time (s)', 'Success Y/N']
	summary_col = ['Session','Finished Session Time','Trials','Hits','Misses', 'Average distance from stimulus center (Px)', 'Avg reaction time (s)', 'Sucesss %']
	reportobj_trial = Report(str(taskname), animal_ID, results_col, 'raw_data')
	reportobj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
	reportobj_trial.createdir()
	reportobj_summary.createdir()
	results = []
	summary = []

	#create stimulus
	grating = visual.GratingStim(win=mywin, size=(1280,720), pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	# limitTrial=3
	trial = 0
	buttons = []
	xpos = 0
	stimPosx = 0
	stimPosy = 0
	ypos = 0
	hits = 0
	size = (1280,720)
	timer = time.time()

	while trial < limitTrial:
		trial = trial+1
		t=time.time() #returns time in sec as float


		grating.draw()
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

	df_results = pd.DataFrame(results, columns=results_col)
	reportobj_trial.writecsv('trial',session)
	average_dist = float(df_results[['Distance from stimulus center (Px)']].mean())
	avg_reactiontime = float(df_results[['Reaction time (s)']].mean())

	session_time = datetime.datetime.now().strftime("%H:%M %p")
	summary.append([session,session_time,limitTrial, hits, limitTrial - hits, average_dist, avg_reactiontime, (float(hits) / float(limitTrial)) * 100])
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
	
	
	
	
	
	


