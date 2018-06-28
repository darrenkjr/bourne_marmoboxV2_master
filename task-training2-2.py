from psychopy import visual, core, logging, event
import time
import random
import marmocontrol as control


def execTask():
	
	limitTrial = 8  # modify
	stepNumber = 4
	delay1 = 1
	delay2 = 0.5
	size = 200
	
	mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)

	transFactor = limitTrial // stepNumber #number of success trials to next lateral translation
	successCounter = 0
	trial = 0
	results = []
	xpos = 0
	ypos = 0
	xtrans = 0

	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 2
	c4 = 0
	c5 = 0
	c6 = 0
	c7 = 0
	
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
				
			if button1 == True:
				control.correctAnswer(False)
				c1 = True

		mywin.update()
		time.sleep(delay1)
		
		# create stimuli
		sPos = [0,0]
		mPos = [xtrans,0]
		nmPos = [0,0]
		ciPos = [0,0]
		crPos = [0,0]
		
		circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=ciPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
		cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=crPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
		
		# show sample

		if c4 < stimLimit and c5 < stimLimit:
			
			a = random.randint(0,1)
			if a == 0:
				sample = circle
				nonmatch = cross
				ciPos = sPos
				crPos = nmPos
				x = 'blue circle'
				c4 += 1
			elif a == 1:
				sample = cross
				nonmatch = circle
				crPos = sPos
				ciPos = nmPos	 	
				x = 'red cross'
				c5 += 1

		elif c4 < stimLimit and c5 == stimLimit:
			a = 0
			sample = circle
			nonmatch = cross
			ciPos = sPos
			crPos = nmPos
			x = 'blue circle'
			c4 += 1

		elif c4 == stimLimit and c5 < stimLimit:
			a = 1
			sample = cross
			nonmatch = circle
			crPos = sPos
			ciPos = nmPos	 	
			x = 'red cross'
			c5 += 1

		sample.draw()
		mywin.update()

		c2 = False
		while c2 == False:	
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button2 = mouse.isPressedIn(sample)

			if button2 == True:
				control.correctAnswer(False)
				c2 = True

		mywin.update()
		time.sleep(delay2)
		
		# forced choice
		
		if c6 < stimLimit and c7 < stimLimit:

			b = random.randint(0,1)
			if b == 0:
				nmPos = [-400,0]
				printPos = 'left'
				c6 += 1
			elif b == 1:
				nmPos = [400,0]
				printPos = 'right'
				c7 += 1

		elif c6 < stimLimit and c7 == stimLimit:
			b = 0
			nmPos = [-400,0]
			printPos = 'left'
			c6 += 1	
			
		elif c6 < stimLimit and c7 == stimLimit:
			b = 1
			nmPos = [400,0]
			printPos = 'right'
			c7 += 1	
		
		if b == 0 and xtrans < 0:
			xtrans *= -1

		elif b == 1 and xtrans > 0:
			xtrans *= -1
			
		if a == 0:
			circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=mPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')
			cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=nmPos, sf=0, color=[1, -1, -1], colorSpace='rgb')
			nonmatch = cross		
		
		elif a == 1:
			circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=nmPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')
			cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=mPos, sf=0, color=[1, -1, -1], colorSpace='rgb')
			nonmatch = circle

		sample.draw()
		nonmatch.draw()
		mywin.update()
		mouse.clickReset()

		trial += 1
		t=time.time()

		c3 = False
		while c3 == False:
		
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button3 = mouse.isPressedIn(sample)
				button4 = mouse.isPressedIn(nonmatch)

			if button3 == True:
				control.correctAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'nmPos: ' + printPos, 'mPos: ' + str(xtrans) + ' px', 'yes'])
				mywin.update()
				time.sleep(3) # ITI for correct
				successCounter += 1
				if successCounter > 0:
					if successCounter % transFactor == 0 and -400 <= xtrans <= 400: #limits of lateral translation
						if xtrans <= 0:
							xtrans -= 100
						elif xtrans >= 0:
							xtrans += 100
				c3 = True 

			elif button4 == True:
				control.incorrectAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'nmPos: ' + printPos, 'mPos: ' + str(xtrans) + ' px', 'no'])
				mywin.update()
				time.sleep(5) # ITI for incorrect
				c3 = True
	
	return results

