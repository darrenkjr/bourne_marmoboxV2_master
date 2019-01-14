from psychopy import visual, core, logging, event
import time, random
import marmocontrol as control
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from reports import Report

def execTask(taskname, mywin, limitTrial, animal_ID):

	#create window
	mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)

	#generating report directory
	results_col = ['Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)', 'Stimulus type','Stimulus Position (Center)','Distance from center (px)', 'Success (Y/N)']
	summary_col = ['Minutes','Seconds', 'Trials', 'Hits', 'Misses', 'Average dist from center (Px)', 'Success%']
	reportObj_trial = Report(str(taskname),animal_ID,results_col,'raw_data')
	reportObj_summary = Report(str(taskname), animal_ID, summary_col,'summary_data')
	results = []
	summary = []

	#setting initial parameters
	trial = 0
	xpos = 0
	ypos = 0
	touchTimeout = False
	hits = 0
	size = 200
	x = 0
	printPos = 0
	reward = 0
	stimx = []
	stimy = []
	stim_coord = []
	
	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0

	timer = time.time()
	ts = time.ctime(timer)

	#display colours and position in pseudorandom sequence
	while trial < limitTrial:

		#create report directories
		reportObj_summary.createdir()
		reportObj_trial.createdir()

		#create stimuli
		stimPosx = random.uniform(-540,540)
		stimPosy = random.randint(-260,260)
		blue = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb')
		red = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb')
		yellow = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb')
		mask = visual.GratingStim(win=mywin, size = 300, pos=[stimPosx,stimPosy], opacity = 0.0) 

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
				grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb')
				x = 'blue'
			elif y == 1:
				grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb')
				x = 'red'
			elif y == 2:
				grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb')
				x = 'yellow'
		
		trial = trial+1
		
		mask.draw()
		grating.draw()
		mywin.update()
		mouse.clickReset() #resets a timer for timing button clicks
		checking = False

		while not checking:
			while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed
				touchTimeout = False
				time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
			else: #If pressed
				xpos = mouse.getPos()[0] #Returns current positions of mouse during press
				ypos = mouse.getPos()[1]
				buttons = mouse.isPressedIn(mask) #Returns True if mouse pressed in mask

			if buttons == True:
				if not touchTimeout:
					control.correctAnswer()
					#calculating center position of stimulus and distance of touch fromm stimuli center
					printPos = str(stimPosx) + ',' + str(stimPosy)
					dist_stim = ((stimPosx - xpos)**2 + (stimPosy - ypos)**2)**(1/2)
					stimx.append(stimPosx)
					stimy.append(stimPosy)
					results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, dist_stim, 'yes'])
					reportObj_trial.addEvent(results)
					touchTimeout = True
					checking = True
					hits += 1
				else:
					time.sleep(0.01)

			else:
				if not touchTimeout:
					control.incorrectAnswer()
					printPos = str(stimPosx) + ',' + str(stimPosy)
					stimx.append(stimPosx)
					stimy.append(stimPosy)
					dist_stim = ((stimPosx - xpos) ** 2 + (stimPosy - ypos) ** 2) ** (1 / 2)
					results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, dist_stim, 'no'])
					reportObj_trial.addEvent(results)
					mywin.update()
					core.wait(2) # specifies trial delay in seconds
					touchTimeout = True
					checking = True

			df_results = pd.DataFrame(results, columns = results_col)
			print('See here: \n',df_results)

			#taking pressed data and stimulus data
			pressed = ([df_results['X-Position (Pressed)']], [df_results['Y-Position (Pressed)']])

	totalTime = time.time() - timer
	mins = int(totalTime / 60)
	secs = round((totalTime % 60), 1)
	average_dist = float(df_results[['Distance from center (px)']].mean())
	summary.append([mins,secs, limitTrial,hits, (limitTrial - hits), average_dist, float(hits)/float(limitTrial)*100])
	reportObj_summary.addEvent(summary)

	# creating scatter plots
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter_p = ax.scatter(pressed[0], pressed[1], color='red', label='pressed')

	stim_coord = [stimx, stimy]
	scatter_stim = ax.scatter(stim_coord[0], stim_coord[1], color='blue', marker='x', label='stimulus center')

	# add stimulus squares
	width = size
	height = size

	stim_zipped = zip(*stim_coord)
	for stim_x, stim_y in stim_zipped:
		ax.add_patch(Rectangle(xy=(stim_x - width / 2, stim_y - height / 2), width=width, height=height, linewidth=1,
							   color='blue', fill=False))
	ax.axis('equal')
	fig.legend((scatter_p, scatter_stim),('Pressed','Stimulus Center'))
	fig.show()
	plt.show()

	return results, summary
	


