from psychopy import visual, core, logging, event  # import some libraries from PsychoPy
import time, random
import numpy as np
import marmocontrol as control
# using predefined stuff

pause = control.getParamTrialDelay()
boxSize = 5

def showimage(im1,im2,im3,im4,im5,mywin):
        im1.draw()
        im2.draw()
        im3.draw()
        im4.draw()
        im5.draw()
        mywin.update()
        time.sleep(pause)

def clearscreen(mywin):
        mywin.update()
        time.sleep(pause)
def pickrand(mywin):
	size = boxSize
        y = random.randint(0,5)
        if y == 1:
                correct = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb')
        elif y == 2:
                correct = visual.GratingStim(win=mywin, size=size, pos=[5,5], sf=0, color = [-1,-1,1], colorSpace='rgb')
        elif y == 3:
                correct = visual.GratingStim(win=mywin, size=size, pos=[5,-5], sf=0, color = [-1,-1,1], colorSpace='rgb')
        elif y == 4:
                correct = visual.GratingStim(win=mywin, size=size, pos=[-5,-5], sf=0, color = [-1,-1,1], colorSpace='rgb')
        else:
                correct = visual.GratingStim(win=mywin, size=size, pos=[-5,5], sf=0, color = [-1,-1,1], colorSpace='rgb')
	wrong1 =  visual.GratingStim(win=mywin, size=size, pos=[5,5], sf=0, color = [-1,-1,-1], colorSpace='rgb')
	wrong2 =  visual.GratingStim(win=mywin, size=size, pos=[5,5], sf=0, color = [-1,-1,-1], colorSpace='rgb')
	wrong3 =  visual.GratingStim(win=mywin, size=size, pos=[5,5], sf=0, color = [-1,-1,-1], colorSpace='rgb')
	wrong4 =  visual.GratingStim(win=mywin, size=size, pos=[5,5], sf=0, color = [-1,-1,-1], colorSpace='rgb')
	a = np.array(correct.pos)
	if a[0] == 0:
		wrong1.pos = [5,5]
                wrong2.pos = [5,-5]
                wrong3.pos = [-5,5]
                wrong4.pos = [-5,-5]
        elif a[0] == 5 and a[1] == 5:
                wrong1.pos = [0,0]
                wrong2.pos = [5,-5]
                wrong3.pos = [-5,5]
                wrong4.pos = [-5,-5]
        elif a[0] == 5 and a[1] == -5:
                wrong1.pos = [5,5]
                wrong2.pos = [0,0]
                wrong3.pos = [-5,5]
                wrong4.pos = [-5,-5]
        elif a[0] == -5 and a[1] == 5:
                wrong1.pos = [5,5]
                wrong2.pos = [5,-5]
                wrong3.pos = [0,0]
                wrong4.pos = [-5,-5]
        else:
                wrong1.pos = [5,5]
                wrong2.pos = [5,-5]
                wrong3.pos = [-5,5]
                wrong4.pos = [0,0]

	return correct, wrong1, wrong2, wrong3, wrong4


def execTask(mywin):
    #create a window
#     mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")

    #create some stimuli
    mouse = event.Mouse(win=mywin)
    mouse.clickReset()
    [correct, wrong1, wrong2, wrong3, wrong4] = pickrand(mywin)
    showimage(correct,wrong1,wrong2,wrong3,wrong4,mywin)
    limitTrial=5
    trial = 0
    #overalltime = [0]*(limitTrial)
    buttons = []
    results = []
    xpos = 0
    ypos = 0
    counter = 1
    corrects = [0]*limitTrial
    while trial < limitTrial:

            #keys = event.getKeys()
            #if keys and keys[0] in ['q', 'Q']:
            #    mywin.close()
            #    core.quit()

            counter =0;
            trial = trial+1
            t=time.time()
	    while counter == 0:
                    if mouse.getPressed()[0]:
                            buttons = mouse.isPressedIn(correct)
                            xpos = mouse.getPos()[0]
                            ypos = mouse.getPos()[1]
                            counter = 1


	    if buttons == True:
                    corrects[trial-1] = 1
		    control.correctAnswer()
                    results.append([trial, xpos, ypos, time.time() - t, 'yes'])
            else:
                    corrects[trial-1] = 0
		    control.incorrectAnswer()
                    results.append([trial, xpos, ypos, time.time() - t, 'no'])

	    counter = 0

            #while core.getTime() = False:
            #while buttons[1] == 0:
            #buttons = mouse.getPressed()
            #t1 = time.time()
            #overalltime[trial-1] = t1-t
            mouse.clickReset()
            clearscreen(mywin)
            #draw the stimuli and update the window
            time.sleep(pause)
	    [correct, wrong1, wrong2, wrong3, wrong4] = pickrand(mywin)
	    showimage(correct,wrong1,wrong2,wrong3,wrong4,mywin)

    return results

