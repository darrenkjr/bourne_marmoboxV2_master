from psychopy import visual, core, logging, event
import time
import random
import marmocontrol as control
import numpy as np

def execTask(mywin):
	
	limitTrial = 6  # modify
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
	
	#Sample Stimuli- Gratings
		# create stimuli
	sPos = [0,0]

	circle_sam = visual.GratingStim(win=mywin, mask='circle', size=size, pos=sPos, sf=0, color=[-1, -1, 1], colorSpace='rgb')  # blue
	cross_sam = visual.GratingStim(win=mywin, mask='cross', size=size, pos=sPos, sf=0, color=[1, -1, -1], colorSpace='rgb')  # red
	diamond_sam = visual.Polygon(win=mywin, edges = 4, size = size, pos=sPos, fillColor = [1,1,-1], lineColor = [1,1,-1], fillColorSpace = 'rgb', lineColorSpace = 'rgb') #yellow
	stimulusNames = ['blue circle', 'red cross', 'yellow diamond']
	stimList = [circle_sam,cross_sam,diamond_sam]
	stimCount = list(np.ones(len(stimList), dtype=np.int) * stimLimit)

	left = [-400,0]
	centre = [0,0]
	right = [400,0]
	positions = {'left':left,'centre':centre,'right':right}
	posCount = {'left':posLimit,'centre':posLimit,'right':posLimit}

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

		stim_pick = random.randint(0,len(stimList)-1)
		stimCount[stim_pick] -= 1
		sample = stimList[stim_pick]
		x = stimulusNames[stim_pick]
		if stimCount[stim_pick] <= 0:
			stimList.pop(stim_pick)
			stimulusNames.pop(stim_pick)
			stimCount.pop(stim_pick)

		#Show sample 3 Times
		for _ in range(0,3):
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
		
		time.sleep(mainDelay-delay2)

		# forced choice
		# Three stimuli displayed 
		randPos = random.choice(posCount.keys())
		printPos = randPos
		mPos = positions[randPos]
		posTemp = dict(positions)
		posTemp.pop(randPos)
		nmPos1=posTemp.pop(random.choice(posTemp.keys()))
		nmPos2=posTemp.pop(random.choice(posTemp.keys()))
		posCount[randPos] -= 1
		if posCount[randPos] <= 0:
			posCount.pop(randPos)

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

