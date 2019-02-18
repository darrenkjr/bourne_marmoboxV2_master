from psychopy import visual, core, logging, event
from psychopy.tools.monitorunittools import posToPix 
import time
import marmocontrol as control
import os

def execTask(mywin):
	#create window
	# mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)
	#create stimulus
	grating = visual.GratingStim(win=mywin, size=700, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	imagefilenames = os.listdir('./images')
	imggrating = []
	for filename in imagefilenames:
		imggrating.append(visual.ImageStim(win=mywin, image='./images/'+str(filename), pos=[0,0], size= [400,400]))
	limitTrial=20
	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0
	interval = 5
	touchTimeout = False
	while trial < limitTrial:
		trial = trial+1
		t=time.time() #returns time in sec as float
		imageno = 0
		grating.draw()
		imggrating[imageno].draw()
		mywin.update()
		mouse.clickReset() #resets a timer for timing button clicks
		stimtime = t
		x = True
		while x:
			while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed 
				time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
				touchTimeout = False
				if (time.time() - stimtime) > interval:
					stimtime = time.time()
					if imageno >= len(imggrating)-1:
						imageno = 0
					else:
						imageno +=1
					grating.draw()
					imggrating[imageno].draw()
					mywin.update()
			else: #If pressed
				xpos = mouse.getPos()[0] #Returns current positions of mouse during press
				ypos = mouse.getPos()[1]
				buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating

			if buttons == True:
				if not touchTimeout:
					control.correctAnswer()
					results.append([trial, xpos, ypos, time.time() - t, '-', 'yes'])
					touchTimeout = True
					x = False
				else:
					time.sleep(0.01)
			else:
				control.incorrectAnswer()
				results.append([trial, xpos, ypos, time.time() - t, '-', 'no'])
				mywin.update()
				core.wait(2) # specifies touchTimeout period
				x = False
   
	return results
