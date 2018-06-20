from psychopy import visual, core, logging, event
import time, random
import marmocontrol as control

def execTask():

	#create window
	mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")
	mouse = event.Mouse(win=mywin)
	
    	limitTrial = 21 #modify
	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0
	
	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0

	#run trials in pseudorandom sequence
	while trial < limitTrial: 

		if c1 < stimLimit and c2 < stimLimit and c3 < stimLimit:
			y = random.randint(0,2)
			if y == 0:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
				x = 'blue' 		
				c1 += 1
			elif y == 1:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
				x = 'red' 		
				c2 += 1
			elif y == 2:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
				x = 'yellow' 		
				c3 += 1
		elif c1 == stimLimit and c2 < stimLimit and c3 < stimLimit:
			y = random.randint(0,1)
			if y == 0:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
				x = 'red' 		
				c2 += 1
			else:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
				x = 'yellow' 		
				c3 += 1				
		elif c1 < stimLimit and c2 == stimLimit and c3 < stimLimit:
			y = random.randint(0,1)
			if y == 0:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
				x = 'blue' 		
				c1 += 1
			else:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
				x = 'yellow' 		
				c3 += 1
		elif c1 < stimLimit and c2 < stimLimit and c3 == stimLimit:
			y = random.randint(0,1)
			if y == 0:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
				x = 'blue' 		
				c1 += 1
			else:
				grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
				x = 'red' 		
				c2 += 1
		elif c1 == stimLimit and c2 == stimLimit and c3 < stimLimit:
			grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
			x = 'yellow' 		
			c3 += 1
		elif c1 < stimLimit and c2 == stimLimit and c3 == stimLimit:
			grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
			x = 'blue' 		
			c1 += 1
		elif c1 == stimLimit and c2 < stimLimit and c3 == stimLimit:
			grating = visual.GratingStim(win=mywin, size=17, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
			x = 'red' 		
			c2 += 1
		
		counter = 0
		trial = trial+1
		t=time.time() #returns time in sec as float
		
		grating.draw()
		mywin.update()
		mouse.clickReset() #resets a timer for timing button clicks
		
		while counter == 0:
				if mouse.getPressed()[0]: # Returns whether mouse button (i.e. button '0') was pressed 
					xpos = mouse.getPos()[0] #Returns current positions of mouse during press
					ypos = mouse.getPos()[1]
					buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating
					counter = 1
		if buttons == True:
			control.correctAnswer()
			results.append([trial, xpos, ypos, time.time() - t, x, 'yes'])
			mywin.update()
		else:
			control.incorrectAnswer()
			results.append([trial, xpos, ypos, time.time() - t, x, 'no'])
			mywin.update()
			pause = core.wait(2) # specifies trial delay
   
	return results
	
	
	
	
	
	


