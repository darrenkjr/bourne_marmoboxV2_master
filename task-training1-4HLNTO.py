from psychopy import visual, core, logging, event
import time, random
import marmocontrol as control

def execTask(mywin):

	#create window
	# mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)
	
    	limitTrial = 100 #modify
    	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0
    	size = 400
	
	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0

	#display colours and position in pseudorandom sequence
	while trial < limitTrial: 

		#create stimuli
		stimPosx = random.uniform(-540,540)
		stimPosy = random.randint(-260,260)
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
		
		trial = trial+1
		t=time.time() #returns time in sec as float
		
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
				buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating

			if buttons == True:
				if not touchTimeout:
					control.correctAnswer()
					printPos = str(stimPosx) + ',' + str(stimPosy)
					results.append([trial, xpos, ypos, time.time() - t, x, printPos, 'yes'])
					touchTimeout = True
					checking = True
					#mywin.update()
				else:
					time.sleep(0.01)

			else:
				control.incorrectAnswer()
				printPos = str(stimPosx) + ',' + str(stimPosy)
				results.append([trial, xpos, ypos, time.time() - t, x, printPos, 'no'])
				checking = True
				mywin.update()
   
	return results
	
	
	
	
	
	


