from psychopy import visual, core, logging, event # import some libraries from$
import time, random
import numpy as np
import marmocontrol as control

pause = control.getParamTrialDelay()
boxSize = 5

def showimage(im1,mywin):
        im1.draw()
        mywin.update()
def clearscreen():
        mywin.update()
        time.sleep(.2)

def pickrand(mywin):
        size = boxSize
        y = random.randint(1,6)
	if y == 1:
                im = visual.GratingStim(win=mywin, size=size,sf=0,  color = [-1,-1,1], colorSpace='rgb')
        elif y == 2:
                im  = visual.GratingStim(win=mywin,mask='circle', size=size,sf=0,  color = [1,-1,-1], colorSpace='rgb')
        elif y == 3:
                im = visual.Polygon(win=mywin, edges = 5, radius = round(size/2),  fillColor = 'purple')
        elif y == 4:
		im = visual.Polygon(win=mywin,edges = 3, radius = round(size/2), fillColor = 'yellow')
        else:
		im  = visual.GratingStim(win=mywin,mask='cross', size=size,sf=0, color =[-1,1,-1] , colorSpace='rgb')
	return im, y

def execTask(mywin):

#     mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")

    #create some stimuli
    mouse = event.Mouse(win=mywin)
    sampling = .001 # in secs
    timeDelay = 1 # in sec
    buttons = []
    results = []
    xpos = 0
    ypos = 0
    mouse.clickReset()
    correct = 3
    success = 0
    realsuccess = 5
    myCounter = 0
    maxCounter = timeDelay
    while realsuccess>success:
	    [im,x]=pickrand(mywin)
	    showimage(im,mywin)
	    mouse.clickReset()
            t = time.time()
	    while myCounter < maxCounter:
		    if mouse.getPressed()[0] == 1:
                            xpos = mouse.getPos()[0]
                            ypos = mouse.getPos()[1]
			    buttons = mouse.isPressedIn(im)
			    if buttons == True and x == correct:
				    myCounter = maxCounter
				    control.correctAnswer()
                                    results.append([success, xpos, ypos, time.time() - t, 'yes'])
				    success = success+1
			    else:
				    control.incorrectAnswer()
                                    results.append([success, xpos, ypos, time.time() - t, 'no'])
				    myCounter = maxCounter
			    buttons = mouse.clickReset()

		    myCounter = myCounter + sampling
		    time.sleep(sampling)
	    myCounter = 0
            mouse.clickReset()

    return results


