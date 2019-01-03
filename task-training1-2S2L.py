from psychopy import visual, core, logging, event
from psychopy.tools.monitorunittools import posToPix 
import time, random
import marmocontrol as control
#from reports import Report

def execTask(mywin):

    #create window
    # mywin = visual.Window([1280,720], monitor="testMonitor", units="pix")
    #reportobj = Report('training1-1','testanimal')
    mouse = event.Mouse(win=mywin)

    #create stimulus
    limitTrial=50
    trial = 0
    buttons = []
    results = []
    xpos = 0
    ypos = 0
    touchTimeout = False
    hits = 0
    size = 300
	
    stimLimit = limitTrial // 3
    c1 = 0
    c2 = 0
    c3 = 0

    timer = time.time()

    while trial < limitTrial:
	
        if c1 < stimLimit and c2 < stimLimit and c3 < stimLimit:
            y = random.randint(0,2)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            elif y == 1:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
            elif y == 2:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 < stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1				
        elif c1 < stimLimit and c2 == stimLimit and c3 < stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 		
                c3 += 1
        elif c1 < stimLimit and c2 < stimLimit and c3 == stimLimit:
            y = random.randint(0,1)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
                c1 += 1
            else:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
                c2 += 1
        elif c1 == stimLimit and c2 == stimLimit and c3 < stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
            x = 'yellow' 		
            c3 += 1
        elif c1 < stimLimit and c2 == stimLimit and c3 == stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
            x = 'blue' 		
            c1 += 1
        elif c1 == stimLimit and c2 < stimLimit and c3 == stimLimit:
            grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
            x = 'red' 		
            c2 += 1
        
        elif c1 == stimLimit and c2 == stimLimit and c3 == stimLimit: #if trial number is not divisible by three, select remainders at random
            y = random.randint(0,2)
            if y == 0:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [-1,-1,1], colorSpace='rgb') 		
                x = 'blue' 		
            elif y == 1:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,-1,-1], colorSpace='rgb') 		
                x = 'red' 		
            elif y == 2:
                grating = visual.GratingStim(win=mywin, size=size, pos=[0,0], sf=0, color = [1,1,-1], colorSpace='rgb') 		
                x = 'yellow' 
            
        trial = trial+1
        
       # reportobj.addEvent('Draw Stimulus Cross. Trial: ' + str(trial))
        #reportobj.save()

        grating.draw()
        mywin.update()
        mouse.clickReset() #resets a timer for timing button clicks
        checking = False
        while not checking:
            while not mouse.getPressed()[0]:# checks whether mouse button (i.e. button '0') was pressed 
                touchTimeout = False
                time.sleep(0.01) # Sleeps if not pressed and then checks again after 10ms
            else: #If pressed
                xpos = mouse.getPos()[0] #Returns current positions of mouse during press
                ypos = mouse.getPos()[1]
                buttons = mouse.isPressedIn(grating) #Returns True if mouse pressed in grating

            if buttons == True:
                if not touchTimeout:
                    control.correctAnswer()
                    results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, 'yes'])
                   # reportobj.addEvent('Mouse Correct')
                    touchTimeout = True
                    checking = True
                    hits += 1
                else:
                    time.sleep(0.01)
            else:
                if not touchTimeout:
                    control.incorrectAnswer()
                    results.append([trial, xpos, ypos, round(time.time() - timer, 4), x, 'no'])
                    mywin.update()
                   # reportobj.addEvent('Mouse InCorrect')
                    core.wait(2) # specifies timeout period
                    touchTimeout = True
                    checking = True
                    
           # reportobj.save()
   
    totalTime = time.time() - timer
    mins = int(totalTime / 60)
    secs = round((totalTime % 60), 1)
    finalResults = '\nMain Results: \n\n' + str(mins) + ' mins ' + str(secs) + ' secs, ' + str(limitTrial) + ' trials, ' + str(hits) + ' hits, ' + str(limitTrial - hits) + ' misses, ' + str("{:.2%}".format(float(hits)/float(limitTrial))) + ' success\n'
    print(finalResults)
    
    return results

