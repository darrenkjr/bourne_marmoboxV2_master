from psychopy import visual, core, logging, event
import time
import random
import marmocontrol as control


def execTask():

	limitTrial = 20  # modify
	delay1 = 1
	delay2 = 0.5
	size = 200

	mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)

	trial = 0
	buttons = []
	results = []
	xpos = 0
	ypos = 0

	while trial < limitTrial:
		
		# show warning

		warning = visual.GratingStim(win=mywin, size=size, pos=[0, 0], sf=0, color=[-1, -1, -1], colorSpace='rgb')
		warning.draw()
		mywin.update()

		c1 = False
		while c1 == False:
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button1 = mouse.isPressedIn(warning)

			if button1 == False:
				control.incorrectAnswer()
			elif button1 == True:
					control.correctAnswer()
					c1 = True

		mywin.update()
		time.sleep(delay1)

		# create stimuli

		mPos = [0,0]
		nmPos = [0,0]
		ciPos = [0,0]
		crPos = [0,0]
		
		circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=ciPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
		cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=crPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
		#sampleCover = visual.GratingStim(win=mywin, size=size, pos=mPos, sf=0, color=[-1, -1, -1], colorSpace='rgb')  # check if necessary
		#nmCover = visual.GratingStim(win=mywin, size=size, pos=nmPos, sf=0, color=[-1, -1, -1], colorSpace='rgb')
		
		# show sample

		a = random.randint(0, 1)  # try to pseudo-randomize later
		if a == 0:
			sample = circle
			nonmatch = cross
			ciPos = mPos
			crPos = nmPos
			x = 'blue circle'
		elif a == 1:
			sample = cross
			nonmatch = circle
			crPos = mPos
			ciPos = nmPos
			x = 'red cross'

		sample.draw()
		#sampleCover.draw()  # check if necessary
		mywin.update()

		c2 = False
		while c2 == False:	
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button2 = mouse.isPressedIn(sample) #changed from sampleCover
			if button2 == False:
				control.incorrectAnswer() 
			elif button2 == True:
				control.correctAnswer()
				c2 = True

		mywin.update()
		time.sleep(delay2)
		
		# forced choice
		
		b = random.randint(0,1)
		if b == 0:
			nmPos = [-400,0] #left of target - modify
			printPos = 'left'
		else:
			nmPos = [400,0] #right of target - modify
			printPos = 'right'
			
		circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=nmPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
		cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=nmPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
		#sampleCover = visual.GratingStim(win=mywin, size=size, pos=mPos, sf=0, color=[-1, -1, -1], colorSpace='rgb')  # check if necessary
		#nmCover = visual.GratingStim(win=mywin, size=size, pos=nmPos, sf=0, color=[-1, -1, -1], colorSpace='rgb')
		
		if a == 0:
			nonmatch = cross

		elif a == 1:
			nonmatch = circle
		
		sample.draw()
		nonmatch.draw()
		#sampleCover.draw()
		#nmCover.draw()
		mywin.update()
		mouse.clickReset()

		trial += 1
		t=time.time()

		c3 = False
		while c3 == False:
		
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button3 = mouse.isPressedIn(sample) #changes
				button4 = mouse.isPressedIn(nonmatch) #changes

			if button3 == True:
				control.correctAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'nmPos: ' + printPos, 'yes'])
				mywin.update()
				time.sleep(3) # ITI for correct
				c3 = True 
			elif button4 == True:
				control.incorrectAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'nmPos: ' + printPos, 'no'])
				mywin.update()
				time.sleep(5) # ITI for incorrect
				c3 = True
	
	return results


# NOTES:    
# display warning 
# warning touched, delay1
# display sample (cross or circle, pseudorandomised)
# sample touched, delay2
# display matching sample (centre) and nonmatching sample (left or right, pseudorandomised)
# NB touching background does not affect task.
