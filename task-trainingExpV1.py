from psychopy import visual, core, logging, event  # import some libraries from PsychoPy
import time
import marmocontrol as control

pause = control.getParamTrialDelay()

def execTask(mywin):
    #create a window
    # mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")
    #pause = s.pauseTime()
    #create some stimuli
    mouse = event.Mouse(win=mywin)
    size = 20
    grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
    #draw the stimuli and update the window
    grating.draw()
    mywin.update()
    mouse.clickReset()
    limitTrial=15
    trial = 0
    #overalltime = [0]*(limitTrial+1)
    buttons = []
    results = []
    xpos = 0
    ypos = 0
    #correct = [0]*(limitTrial+1)
    while trial < limitTrial:
	    trial = trial+1
	    t=time.time()
        while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed 
			time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
		else: #If pressed
			xpos = mouse.getPos()[0] #Returns current positions of mouse during press
			ypos = mouse.getPos()[1]
			buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating
            
	    if buttons == True:
		    #correct[trial-1] = 1
		    size = size-1
		    control.correctAnswer()
                    results.append([trial, xpos, ypos, time.time() - t, 'yes'])
	    else:
		    #correct[trial] = 0
		    control.incorrectAnswer()
                    results.append([trial, xpos, ypos, time.time() - t, 'no'])

	    #if grating.contains(mouse):
        	    #print('pressed')

            #while core.getTime() = False:
	    #while buttons[1] == 0:
	    #buttons = mouse.getPressed()
	    #t1 = time.time()
	    #overalltime[trial-1] = t1-t
	    mouse.clickReset()
	    grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb' )
	    #draw the stimuli and update the window
	    grating.draw()
	    mywin.update()
	    time.sleep(pause)
    
    return results


