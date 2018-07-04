from psychopy import visual, core, logging, event
import time
import random
import marmocontrol as control

def execTask(mywin):
	
	limitTrial = 12  # modify
	mainDelay = 1
	delay1 = 1
	delay2 = 0.5
	size = 200
	
	# mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix")
	mouse = event.Mouse(win=mywin)
	
	trial = 0
	results = []
	xpos = 0
	ypos = 0

	#set stimuli limit and trial counter variables
	stimLimit = limitTrial // 3
	posLimit = limitTrial // 3
	c8 = 0 #match left
	c7 = 0 #match centre
	c9 = 0 #match right
	
	#Sample Stimuli- Gratings
		# create stimuli
	sPos = [0,0]

	circle_sam = visual.GratingStim(win=mywin, mask='circle', size=size, pos=sPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
	cross_sam = visual.GratingStim(win=mywin, mask='cross', size=size, pos=sPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
	diamond_sam = visual.Polygon(win=mywin, edges = 4, size = size, pos=sPos, fillColor = [1,1,-1], lineColor = [1,1,-1], fillColorSpace = 'rgb', lineColorSpace = 'rgb') #yellow
	stimulusNames = ['blue circle', 'red cross', 'yellow diamond']
	stimList = [circle_sam,cross_sam,diamond_sam]
	stimulus_list = []
	for i in range(len(stimulusNames)):
		for j in range(stimLimit):
			stimulus_list.append(i)

	warning = visual.GratingStim(win=mywin, size=size, pos=[0, 0], sf=0, color=[-1, -1, -1], colorSpace='rgb')
	
	while trial < limitTrial:
		
		# show warning
		warning.draw()
		mywin.update()
		# Wait for mouse l
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

		# show sample
		stim_pick = stimulus_list.pop(random.randint(0,len(stimulus_list)-1))
		sample = stimList[stim_pick]
		x = stimulusNames[stim_pick]
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

		# show sample again

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

		# show sample a third time

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
		time.sleep(mainDelay)

		# forced choice
		
		left = [-400,0]
		centre = [0,0]
		right = [400,0]

		d = random.randint(0,1)

		if c7 < posLimit and c8 < posLimit and c9 < posLimit:

			b = random.randint(0,2)

			if b == 0:
				mPos = left
				printPos = 'left'
				c7 += 1
				if d == 0:
					nmPos1 = centre
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = centre

			elif b == 1:
				mPos = centre
				printPos = 'centre'
				c8 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = left

			elif b == 2:
				mPos = right
				printPos = 'right'
				c9 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = centre
				else:
					nmPos1 = centre
					nmPos2 = left

		elif c7 == stimLimit and c8 < stimLimit and c9 < stimLimit:

			b = random.randint(0,1)

			if b == 0:
				mPos = centre
				printPos = 'centre'
				c8 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = left

			elif b == 1:
				mPos = right
				printPos = 'right'
				c9 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = centre
				else:
					nmPos1 = centre
					nmPos2 = left

		elif c7 < stimLimit and c8 == stimLimit and c9 < stimLimit:

			b = random.randint(0,1)

			if b == 0:
				mPos = left
				printPos = 'left'
				c7 += 1
				if d == 0:
					nmPos1 = centre
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = centre
			
			elif b == 1:
				mPos = right
				printPos = 'right'
				c9 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = centre
				else:
					nmPos1 = centre
					nmPos2 = left		

		elif c7 < stimLimit and c8 < stimLimit and c9 == stimLimit:

			b = random.randint(0,1)

			if b == 0:
				mPos = left
				printPos = 'left'
				c7 += 1
				if d == 0:
					nmPos1 = centre
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = centre

			elif b == 1:
				mPos = centre
				printPos = 'centre'
				c8 += 1
				if d == 0:
					nmPos1 = left
					nmPos2 = right
				else:
					nmPos1 = right
					nmPos2 = left

		elif c7 == stimLimit and c8 == stimLimit and c9 < stimLimit:

			mPos = right
			printPos = 'right'
			c9 += 1
			if d == 0:
				nmPos1 = left
				nmPos2 = centre
			else:
				nmPos1 = centre
				nmPos2 = left

		elif c7 < stimLimit and c8 == stimLimit and c9 == stimLimit:
		
			mPos = left
			printPos = 'left'
			c7 += 1
			if d == 0:
				nmPos1 = centre
				nmPos2 = right
			else:
				nmPos1 = right
				nmPos2 = centre

		elif c7 == stimLimit and c8 < stimLimit and c9 == stimLimit:

			mPos = centre
			printPos = 'centre'
			c8 += 1
			if d == 0:
				nmPos1 = left
				nmPos2 = right
			else:
				nmPos1 = right
				nmPos2 = left

#smooth out diamond position errors

		if x == 'blue circle':
			ciPos = mPos
			crPos = nmPos1
			trPos = nmPos2
			#trPos[1] = -30
			circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=ciPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
			cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=crPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
			diamond = visual.Polygon(win=mywin, edges = 4, pos=trPos, size = size, fillColor = [1,1,-1], lineColor = [1,1,-1], fillColorSpace = 'rgb', lineColorSpace = 'rgb') #yellow
			match = circle
			nonmatch1 = cross
			nonmatch2 = diamond

		elif x == 'red cross':
			crPos = mPos
			ciPos = nmPos1
			trPos = nmPos2
			#trPos[1] = -30
			circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=ciPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
			cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=crPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
			diamond = visual.Polygon(win=mywin, edges = 4, pos=trPos, size = size, fillColor = [1,1,-1], lineColor = [1,1,-1], fillColorSpace = 'rgb', lineColorSpace = 'rgb') #yellow
			match = cross
			nonmatch1 = circle
			nonmatch2 = diamond

		elif x == 'yellow diamond':
			trPos = mPos
			#trPos[1] = -30
			ciPos = nmPos1
			crPos = nmPos2
			circle = visual.GratingStim(win=mywin, mask='circle', size=size, pos=ciPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
			cross = visual.GratingStim(win=mywin, mask='cross', size=size, pos=crPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
			diamond = visual.Polygon(win=mywin, edges = 4, pos=trPos, size = size, fillColor = [1,1,-1], lineColor = [1,1,-1], fillColorSpace = 'rgb', lineColorSpace = 'rgb') #yellow
			match = diamond
			nonmatch1 = circle
			nonmatch2 = cross

		match.draw()
		nonmatch1.draw()
		nonmatch2.draw()
		mywin.update()
		mouse.clickReset()

		trial += 1
		t=time.time()

		c3 = False
		while c3 == False:
		
			while not mouse.getPressed()[0]:
				time.sleep(0.01)
			else:
				button3 = mouse.isPressedIn(match)
				button4 = mouse.isPressedIn(nonmatch1)
				button5 = mouse.isPressedIn(nonmatch2)

			if button3 == True:
				control.correctAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'mPos: ' + printPos, 'yes'])
				mywin.update()
				time.sleep(3) # ITI for correct
				c3 = True 

			elif button4 == True or button5 == True:
				control.incorrectAnswer()
				xpos = mouse.getPos()[0]
				ypos = mouse.getPos()[1]
				results.append([trial, xpos, ypos, time.time() - t, x, 'mPos: ' + printPos, 'no'])
				mywin.update()
				time.sleep(5) # ITI for incorrect
				c3 = True
	
	return results

