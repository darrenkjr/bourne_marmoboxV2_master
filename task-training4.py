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
    	size = 4 #make consistent with task-training3.py
	
	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0

	#display colours and position in pseudorandom sequence
	while trial < limitTrial: 

		#create stimuli
		stimPosx = random.uniform(-15.0,15.0)
		stimPosy = random.randint(-7.0,7.0)
		blue = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [-1,-1,1], colorSpace='rgb')
		red = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,-1,-1], colorSpace='rgb')
		yellow = visual.GratingStim(win=mywin, size=size, pos=[stimPosx,stimPosy], sf=0, color = [1,1,-1], colorSpace='rgb')
		 

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
		
		

		counter = 0
		trial = trial+1
		t=time.time() #returns time in sec as float
		
		grating.draw()
		mywin.update()
		mouse.clickReset() #resets a timer for timing button clicks
		
		while counter == 0:
				if mouse.getPressed()[0]: # Returns whether mouse button was pressed 
					xpos = mouse.getPos()[0] #Returns current positions of mouse during press
					ypos = mouse.getPos()[1]
					buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating
					counter = 1
		if buttons == True:
			control.correctAnswer()
			printsize = str(size) and ' degrees' #need to report location instead of printsize!
			results.append([trial, xpos, ypos, time.time() - t, x, printsize, 'yes'])
			mywin.update()

		else:
			control.incorrectAnswer()
			printsize = str(size) and ' degrees' #and here too
			results.append([trial, xpos, ypos, time.time() - t, x, printsize, 'no'])
			mywin.update()
			core.wait(2) # specifies trial delay
   
	return results
	
	
	
	
	
	


