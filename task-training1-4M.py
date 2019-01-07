from psychopy import visual, core, logging, event
import time, random
import marmocontrol as control
import pandas as pd

def execTask(mywin):

	#create window
	# mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)
	
    	limitTrial = 3 #modify
    	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0
	touchTimeout = False
	hits = 0
    	size = 200
	
	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	c1 = 0
	c2 = 0
	c3 = 0
    
    	timer = time.time()
	
	#display colours and position in pseudorandom sequence
	while trial < limitTrial: 

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
					printPos = str(stimPosx) + ',' + str(stimPosy)
					results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, 'yes'])
                    			touchTimeout = True
                    			checking = True
                    			hits += 1
                		else:
                    			time.sleep(0.01)

			else:
                		if not touchTimeout:
					control.incorrectAnswer()
					printPos = str(stimPosx) + ',' + str(stimPosy)
					results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, printPos, 'no'])
					mywin.update()
					core.wait(2) # specifies trial delay
					touchTimeout = True
					checking = True	

    	totalTime = time.time() - timer
 	mins = int(totalTime / 60)
    	secs = round((totalTime % 60), 1)
    	finalResults = '\nMain Results: \n\n' + str(mins) + ' mins ' + str(secs) + ' secs, ' + str(limitTrial) + ' trials, ' + str(hits) + ' hits, ' + str(limitTrial - hits) + ' misses, ' + str("{:.2%}".format(float(hits)/float(limitTrial))) + ' success\n'
    	print(finalResults)

	results_col = ['trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time', 'x','Stimulus Position', 'Success (Y/N)' ]
	df = pd.DataFrame(results, columns=["results_col"])
	df.to_csv('test.csv', index=False)

	return results




	
	


