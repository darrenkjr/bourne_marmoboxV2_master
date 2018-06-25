
from psychopy import visual
import marmobox
import marmocontrol
mywin = visual.Window([1600,960], monitor="testMonitor", units="deg", pos = (0,0))
while 1:
#    mywin = visual.Window([1600,960], monitor="testMonitor", units="deg", pos = (0,0))
   # mywin.flip()
    print('Background display initiated.')
    r = raw_input('Manual Reward? (y/n): ')
    if r == 'y':
#        while r == 'y':
         marmocontrol.reward()
         print('Reward delivered.')
#            r = raw_input('Manual Reward? (y/n): ')
#	else:
#           mywin.close()
#           marmobox.run(taskname,delay)
    elif r == 'n':
        taskname = raw_input('Select Task: ')
        delay = input('Set Delay: ')
        try:
            mywin.close()
            marmobox.run(taskname,delay)
        except:
            marmocontrol.force_stop()
            print 'An error occured.'
        finally:
             mywin = visual.Window([1600,960], monitor="testMonitor", units="deg", pos = (0,0))

	   
	      

