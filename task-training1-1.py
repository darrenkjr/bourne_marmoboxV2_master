from psychopy import visual, core, logging, event
import time
import marmocontrol as control
from reports import Report
from heatmap import Heatmap
import pandas as pd
import matplotlib.pyplot as plt

def execTask(taskname, mywin, limitTrial, animal_ID):

	mouse = event.Mouse(win=mywin)

	# generating report directories and object
	results_col = ['Trial', 'xpos', 'ypos', 'Time (s)', '-', 'Distance from stimulus center (Px)', 'Success Y/N']
	summary_col = ['Trials','Hits','Misses', 'Average distance from stimulus center (Px)', 'Sucesss %']
	reportobj_trial = Report(str(taskname), animal_ID, results_col, 'raw_data')
	reportobj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
	reportobj_trial.createdir()
	reportobj_summary.createdir()

	results = []
	summary = []

	#create stimulus
	grating = visual.GratingStim(win=mywin, size=700, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	# limitTrial=3
	trial = 0
	buttons = []
	xpos = 0
	stimPosx = 0
	stimPosy = 0
	ypos = 0
	hits = 0
	size = 700



	while trial < limitTrial:
		trial = trial+1
		t=time.time() #returns time in sec as float


		grating.draw()
		mywin.update()
		mouse.clickReset() #resets a timer for timing button clicks
		
		while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed 
			time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
		else: #If pressed
			xpos = mouse.getPos()[0] #Returns current positions of mouse during press
			ypos = mouse.getPos()[1]
			buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating

		if buttons == True:
			control.correctAnswer()
			dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2)
			results.append([trial, xpos, ypos, time.time() - t, '-', dist_stim, 'yes'])
			reportobj_trial.addEvent(results)
			hits += 1
		else:
			control.incorrectAnswer()
			dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2)
			results.append([trial, xpos, ypos, time.time() - t, '-', dist_stim, 'no'])
			mywin.update()
			reportobj_trial.addEvent(results)
			core.wait(2) # specifies timeout period

	df_results = pd.DataFrame(results, columns=results_col)
	reportobj_trial.writecsv()
	average_dist = float(df_results[['Distance from stimulus center (Px)']].mean())


	summary.append([limitTrial, hits, limitTrial - hits, average_dist, (float(hits) / float(limitTrial)) * 100])
	reportobj_summary.addEvent(summary)
	reportobj_summary.writecsv()

	print('Summary Results: \n' + str(limitTrial) + ' trials, ' + str(hits) + ' hits, ' + str(limitTrial - hits) + ' misses, ' + str("{:.2%}".format(float(hits)/float(limitTrial))) + ' success')
	print('Raw results: \n', df_results)

	#organizing coordinates
	pressed = ([df_results['xpos']], [df_results['ypos']])
	stimulus = ([stimPosx],[stimPosy])
	#creating scatter object
	scatter = Heatmap(stimulus,pressed,size)
	heatmap, xedges, yedges = scatter.heatmap(limitTrial)

	#plotting heatmap
	plt.imshow(heatmap.T, interpolation='bicubic', cmap=plt.cm.Reds, extent=[xedges[0],xedges[-1],yedges[0],yedges[-1]], origin = 'lower')
	plt.show()

	print(summary)
	return results
	
	
	
	
	
	
	


