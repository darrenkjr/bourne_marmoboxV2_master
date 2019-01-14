from psychopy import visual, core, logging, event
import time
import marmocontrol as control
from reports import Report

def execTask(taskname, mywin, limitTrial, animal_ID):

	#create window
	# mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")

	#creating report object and directory
	results_col = ['Trial', 'xpos', 'ypos', 'Time (s)', '-', 'Success Y/N']
	reportobj = Report(str(taskname),animal_ID, results_col,'raw_data')
	reportobj.createdir()
	mouse = event.Mouse(win=mywin)

	#create stimulus
	grating = visual.GratingStim(win=mywin, size=(1280,720), pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	#limitTrial=40
	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0

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
			results.append([trial, xpos, ypos, time.time() - t, '-', 'yes'])
			#add results to event module as a list
			reportobj.addEvent(results)
		else:
			control.incorrectAnswer()
			results.append([trial, xpos, ypos, time.time() - t, '-', 'no'])
			mywin.update()
			reportobj.addEvent(results)
			core.wait(2) # specifies timeout period
	return results
	
	
	
	
	
	


