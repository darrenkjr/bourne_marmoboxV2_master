from psychopy import visual, core, logging, event
import time
import marmocontrol as control
from reports import Report
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np

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
	average_dist = float(df_results[['Distance from stimulus center (Px)']].mean())


	summary.append([limitTrial, hits, limitTrial - hits, average_dist, (float(hits) / float(limitTrial)) * 100])
	reportobj_summary.addEvent(summary)

	print('Summary Results: \n' + str(limitTrial) + ' trials, ' + str(hits) + ' hits, ' + str(limitTrial - hits) + ' misses, ' + str("{:.2%}".format(float(hits)/float(limitTrial))) + ' success')
	print('Raw results: \n', df_results)

	#creating scatter plots, taking pressed data and stimulus data
	pressed = ([df_results['xpos']], [df_results['ypos']])
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter_p = ax.scatter(pressed[0], pressed[1], color='red', label='pressed', alpha=0)
	scatter_stim = ax.scatter(0, 0, color='blue', marker='o', label='stimulus center', alpha=0)

	# add stimulus squares
	width = size
	height = size
	stim_coord = [[0],[0]]

	stim_zipped = zip(*stim_coord)
	for stim_x, stim_y in stim_zipped:
		ax.add_patch(Rectangle(xy=(stim_x - width / 2, stim_y - height / 2), width=width, height=height, linewidth=1,
							   color='blue', fill=False))
	ax.axis('equal')
	fig.legend((scatter_p, scatter_stim),('Pressed','Stimulus Center'))
	fig.show()
	flat_pressedx = np.array(pressed[0]).ravel()
	flat_pressedy = np.array(pressed[1]).ravel()

	heatmap, xedges,yedges = np.histogram2d(flat_pressedx.ravel(),flat_pressedy.ravel(),range=[[-500,500],[-500,500]],bins=limitTrial)

	plt.imshow(heatmap.T, interpolation='bicubic', cmap=plt.cm.Reds, extent=[xedges[0],xedges[-1],yedges[0],yedges[-1]], origin = 'lower')
	plt.show()

	print(summary)
	return results
	
	
	
	
	
	
	


