from psychopy import visual, core, logging, event
import time, random
import marmocontrol as control

def showimage(im1,mywin):
        im1.draw()
        mywin.update()
        time.sleep(1)
def clearscreen(mywin):
	mywin.update()
        time.sleep(1)

def appendEvent(results, trial, xpos, ypos, time, reward):
    results.append([trial, xpos, ypos, time, reward])

def execTask():

    #create a window
    mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")

    #create some stimuli
    mouse = event.Mouse(win=mywin)
    mouse.clickReset()
    size = 10;
    square = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
    showimage(square,mywin)
    limitTrial=5
    trial = 0
    overalltime = [0]*(limitTrial)
    buttons = []
    counter = 1
    results = []
    xpos = 0
    ypos = 0

    while trial < limitTrial:
	    upcounter=0
            trial = trial+1
            t=time.time()
            while upcounter < counter:
		    if mouse.getPressed()[0]:
                	    buttons = mouse.isPressedIn(square)
                            xpos = mouse.getPos()[0]
                            ypos = mouse.getPos()[1]
        		    if buttons == True:
				    time.sleep(.2)
        			    mouse.clickReset()
				    time.sleep(.2)
				    upcounter = upcounter + 1
				    buttons = False
				    if upcounter == counter:
					    control.correctAnswer()
                                            appendEvent(results, trial, xpos, ypos, time.time() - t, 'yes')
                                    else:
                                            appendEvent(results, trial, xpos, ypos, time.time() - t, 'notyet')
			    else:
				    time.sleep(.2)
                	            mouse.clickReset()
                       		    time.sleep(.2)
				    upcounter = counter
				    counter  = counter - 4
				    control.incorrectAnswer()
                                    appendEvent(results, trial, xpos, ypos, time.time() - t, 'no')
	    clearscreen(mywin)
            showimage(square,mywin) 
	    counter = counter + 4

    return results

