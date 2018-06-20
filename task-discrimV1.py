from psychopy import visual, core, logging, event # import some libraries 
import time, random
import numpy as np
import marmocontrol as control

pause = control.getParamTrialDelay()
boxSize = 5

def showimage(im1,im2,im3,im4,im5,mywin,x):
	if x==1:
       		im1.draw()
                im2.draw()
        elif x==2:
                im1.draw()
                im2.draw()
                im3.draw()
        elif x==3:
                im1.draw()
                im2.draw()
                im3.draw()
                im4.draw()
        else:
                im1.draw()
                im2.draw()
                im3.draw()
                im4.draw()
		im5.draw()
	mywin.update()


def randomAmount(mywin):
        size = boxSize
	x = random.randint(1,5) # chooses the amount of stimuli there is in the exp from 2 to 5
	if x == 1:
		im1 = visual.GratingStim(win=mywin, size=size, pos=[-4,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im2 = visual.GratingStim(win=mywin, size=size, pos=[4,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im3 = 0
		im4 = 0
		im5 = 0
	elif x==2:
		im1 = visual.GratingStim(win=mywin, size=size, pos=[-6,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
                im2 = visual.GratingStim(win=mywin, size=size, pos=[6,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im3 = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im4 = 0
		im5 = 0
	elif x == 3:
                im1 = visual.GratingStim(win=mywin, size=size, pos=[-10,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
                im2 = visual.GratingStim(win=mywin, size=size, pos=[-4,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
                im3 = visual.GratingStim(win=mywin, size=size, pos=[4,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im4 = visual.GratingStim(win=mywin, size=size, pos=[10,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im5 = 0
	else:
		im1 = visual.GratingStim(win=mywin, size=size, pos=[-14,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
                im2 = visual.GratingStim(win=mywin, size=size, pos=[-6,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
                im3 = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im4 = visual.GratingStim(win=mywin, size=size, pos=[6,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
		im5 = visual.GratingStim(win=mywin, size=size, pos=[14,0], sf=0,  color = [1,-1,-1], colorSpace='rgb')
	y = random.randint(0,x) # chooses the posision of correct
	if y == 0:
		im1.color = [-1,-1,1]
	elif y==1:
                im2.color = [-1,-1,1]
                #im2.mask = 'cross'
	elif y==2:
                im3.color = [-1,-1,1]
                #im3.mask = 'cross'
	elif y==3:
                im4.color = [-1,-1,1]
                #im4.mask = 'cross'
	else:
                im5.color = [-1,-1,1]
                #im5.mask = 'cross'

	return im1,im2,im3,im4,im5, x, y

def isCorrect(y, mouse, im1, im2, im3, im4, im5):
	if y == 0:
		buttons = mouse.isPressedIn(im1)
	elif y==1:
		buttons = mouse.isPressedIn(im2)
        elif y==2:
                buttons = mouse.isPressedIn(im3)
        elif y==3:
                buttons = mouse.isPressedIn(im4)
        else:
                buttons = mouse.isPressedIn(im5)
	return buttons




def execTask():
    #create some stimuli

    mywin = visual.Window([1600,960],monitor="testMonitor", units="deg")
    mouse = event.Mouse(win=mywin)

    buttons = []
    results = []
    xpos = 0
    ypos = 0
    mouse.clickReset()
    trial = 0

    while 5>trial:
	    trial += 1
	    counter =0
            [im1,im2,im3,im4,im5,x,y]=randomAmount(mywin)
            showimage(im1,im2,im3,im4,im5,mywin,x)
            mouse.clickReset()
            t = time.time()
	    while counter ==0:
        	    if mouse.getPressed()[0] == 1:
                            xpos = mouse.getPos()[0]
                            ypos = mouse.getPos()[1]
 			    buttons = isCorrect(y, mouse, im1, im2, im3, im4, im5)
			    if buttons == True:
                        	    control.correctAnswer()
                                    results.append([trial, xpos, ypos, time.time() - t, 'yes'])
				    counter = 1
                	    else:
				    counter =1
                         	    control.incorrectAnswer()
                                    results.append([trial, xpos, ypos, time.time() - t, 'no'])
                	    buttons = mouse.clickReset()
            mouse.clickReset()
    return results
