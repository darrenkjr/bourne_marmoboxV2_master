from psychopy import visual, core, logging, event
from psychopy.tools.monitorunittools import posToPix 
import time
import marmocontrol as control

def execTask():

	#create window
	mywin = visual.Window([1600,900], monitor="testMonitor", units="deg")
	mouse = event.Mouse(win=mywin)

	#create stimulus
	grating = visual.GratingStim(win=mywin, size=(3), pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	limitTrial=20
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
		else:
			control.incorrectAnswer()
			results.append([trial, xpos, ypos, time.time() - t, '-', 'no'])
			mywin.update()
			core.wait(2) # specifies timeout period
   
	return results
	
	
	
	
	
	


