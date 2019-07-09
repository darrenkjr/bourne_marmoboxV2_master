from psychopy import visual, core, event
import time, random
from archive import marmocontrol as control
from archive.reports import Report


def execTask(taskname,limitTrial,mywin,animal_ID):

	#create window
	mouse = event.Mouse(win=mywin)

	# generating report directories and objects
	results_col = ['Timestamp','Trial', 'xpos', 'ypos', 'Time (s)', 'Print Size', 'Distance from stimulus center (Px)', 'Reaction time (s)', 'Success Y/N']
	summary_col = ['Finished Session Time','Trials','Hits','Misses', 'Average distance from stimulus center (Px)', 'Avg reaction time (s)', 'Sucesss %']
	reportobj_trial = Report(str(taskname), animal_ID, results_col, 'raw_data')
	reportobj_summary = Report(str(taskname), animal_ID, summary_col, 'summary_data')
	reportobj_trial.createdir()
	reportobj_summary.createdir()
	results = []
	summary = []

	step_number = 5
    reductionFactor = limitTrial // step_number #number of success trials to next size decrease
	successCounter = 0
	trial = 0
	buttons = []
	xpos = 0
	ypos = 0
	initSize = 700
	size = initSize

	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0

	#display colours in pseudorandom sequence
	while trial < limitTrial: 

		#create stimuli
		blue = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb')
		red = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb')
		yellow = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb')

		if c1 < stimLimit and c2 < stimLimit and c3 < stimLimit:
			y = random.randint(0,2)
			if y == 0:
				grating = blue 		
				x = 'blue' 		
				c1 += 1
			elif y == 1:
				grating = red 		
				x = 'red' 		
				c2 += 1
			elif y == 2:
				grating = yellow 		
				x = 'yellow' 		
				c3 += 1
		elif c1 == stimLimit and c2 < stimLimit and c3 < stimLimit:
			y = random.randint(0,1)
			if y == 0:
				grating = red 		
				x = 'red' 		
				c2 += 1
			else:
				grating = yellow 		
				x = 'yellow' 		
				c3 += 1				
		elif c1 < stimLimit and c2 == stimLimit and c3 < stimLimit:
			y = random.randint(0,1)
			if y == 0:
				grating = blue 		
				x = 'blue' 		
				c1 += 1
			else:
				grating = yellow 		
				x = 'yellow' 		
				c3 += 1
		elif c1 < stimLimit and c2 < stimLimit and c3 == stimLimit:
			y = random.randint(0,1)
			if y == 0:
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
			printsize = str(size) + ' degrees'
			results.append([trial, xpos, ypos, time.time() - t, x, printsize, 'yes'])
			mywin.update()
            		successCounter += 1
            		if successCounter > 0:
				    if successCounter % reductionFactor == 0 and size >= 200: # size reduction following successful hit trials or limit
                				size -= ((initSize - 200)/4) # modify
		else:
			control.incorrectAnswer()
			printsize = str(size) + ' degrees'
			results.append([trial, xpos, ypos, time.time() - t, x, printsize, 'no'])
			mywin.update()
			core.wait(2) # specifies trial delay
   
	return results
	
	
	
	
	
	


