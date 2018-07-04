from psychopy import visual, core, logging, event  # import some libraries from PsychoPy
import time, random
import marmocontrol as control
# predefined stuff
boxSize = 5
pause = control.getParamTrialDelay()

def showimage(im1,im2,im3,thumbs,mywin):
	size = boxSize
	coverL = visual.GratingStim(win=mywin, size=size, pos=[10,5], sf=0, color = [-1,-1,-1], colorSpace='rgb' )
	coverR = visual.GratingStim(win=mywin, size=size, pos=[-10,5], sf=0, color = [-1,-1,-1], colorSpace='rgb' )
        coverM = visual.GratingStim(win=mywin, size=size, pos=[0,5], sf=0, color = [-1,-1,-1], colorSpace='rgb' )
	im1.draw()
	mywin.update()
	time.sleep(pause)
        im2.draw()
        mywin.update()
        time.sleep(pause)
        im3.draw()
        mywin.update()
        time.sleep(pause)
	thumbs.draw()
	coverL.draw()
	coverR.draw()
	coverM.draw()
	mywin.update()
	time.sleep(pause)
def pickrand(mywin):
	size = boxSize
	y = random.randint(0,3)
	if y == 1:
		thumbs = visual.GratingStim(win=mywin,mask='circle', size=size, pos=[0,-5], sf=0, color = [1,-1,-1], colorSpace='rgb')
	elif y == 2:
                thumbs = visual.GratingStim(win=mywin, size=size, pos=[0,-5], sf=0, color = [-1,-1,1], colorSpace='rgb')
	else:
                thumbs = visual.GratingStim(win=mywin,mask='cross', size=size, pos=[0,-5], sf=0, color = [-1,1,-1], colorSpace='rgb')
	x=random.randint(0,5)
        if x==1:
               dcorrect = visual.GratingStim(win=mywin, size=size, pos=[10,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
               dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[-10,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
               dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[0,5], sf=0, color = [-1,1,-1], colorSpace='rgb')
        elif x==2:
                dcorrect = visual.GratingStim(win=mywin, size=size, pos=[10,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
                dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[0,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
                dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[-10,5], sf=0, color = [-1,1,-1], colorSpace='rgb' )
        elif x==3:
                dcorrect = visual.GratingStim(win=mywin, size=size, pos=[-10,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
                dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[0,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
                dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[10,5], sf=0, color = [-1,1,-1], colorSpace='rgb' )
        elif x==3:
                dcorrect = visual.GratingStim(win=mywin, size=size, pos=[0,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
                dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[-10,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
                dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[10,5], sf=0, color = [-1,1,-1], colorSpace='rgb' )
        elif x==4:
                dcorrect = visual.GratingStim(win=mywin, size=size, pos=[-10,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
                dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[10,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
                dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[0,5], sf=0, color = [-1,1,-1], colorSpace='rgb' )
        else:
                dcorrect = visual.GratingStim(win=mywin, size=size, pos=[0,5], sf=0, color = [-1,-1,1], colorSpace='rgb' )
                dwrong1 = visual.GratingStim(win=mywin,mask='circle' ,size=size, pos=[10,5], sf=0, color = [1,-1,-1], colorSpace='rgb' )
                dwrong2 = visual.GratingStim(win=mywin,mask='cross' ,size=size, pos=[-10,5], sf=0, color = [-1,1,-1], colorSpace='rgb' )
	if dcorrect.mask == thumbs.mask:
		correct = dcorrect
		wrong1 = dwrong1
		wrong2 = dwrong2
	elif dwrong1.mask == thumbs.mask:
                correct = dwrong1
                wrong1 =  dcorrect
                wrong2 = dwrong2
	else:
                correct = dwrong2
                wrong1 = dwrong1
                wrong2 = dcorrect


	return correct, wrong1, wrong2, thumbs


def execTask(mywin):

    #create a window
#     mywin = visual.Window([1600,960], monitor="testMonitor", units="deg")

    #create some stimuli
    mouse = event.Mouse(win=mywin)

    correct, wrong1, wrong2, thumbs = pickrand(mywin)

    showimage(correct,wrong1,wrong2,thumbs,mywin)

    mouse.clickReset()
    limitTrial=5
    trial = 0
    #overalltime = [0]*(limitTrial)
    buttons = []
    results = []
    posx = 0
    posy = 0
    #corrects = [0]*(limitTrial)
    while trial < limitTrial:
            counter =0;
            trial = trial+1
            t=time.time()
            while counter == 0:
                    if mouse.getPressed()[0]:
                            buttons = mouse.isPressedIn(correct)
                            posx = mouse.getPos()[0]
                            posy = mouse.getPos()[1]
                            counter = 1
            if buttons == True:
                    #corrects[trial-1] = 1
		    control.correctAnswer()
                    results.append([trial, posx, posy, time.time() - t, 'yes'])
            else:
                    #corrects[trial-1] = 0
		    control.incorrectAnswer()
                    results.append([trial, posx, posy, time.time() - t, 'no'])

            #if correct.contains(mouse):
            #        print('pressed')

            #while core.getTime() = False:
            #while buttons[1] == 0:
            #buttons = mouse.getPressed()
            #t1 = time.time()
            #overalltime[trial-1] = t1-t
            mouse.clickReset()
	    mywin.update()
            #draw the stimuli and update the window
            time.sleep(1)
	    correct, wrong1, wrong2, thumbs = pickrand(mywin)
	    showimage(correct,wrong1,wrong2,thumbs,mywin)

    return results


