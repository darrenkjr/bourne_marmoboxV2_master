from psychopy import visual
import marmobox
import marmocontrol
mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos = (0,0))
while 1:
    print('Background display initiated.')
    r = raw_input('Manual Reward? (y/n): ')
    if r == 'y':
        marmocontrol.reward()
        print('Reward delivered.')
    elif r == 'n':
        taskname = raw_input('Select Task: ')
        delay = input('Set Delay: ')
        try:
            marmobox.run(taskname,delay,mywin)
        except:
            mywin.close()
            marmocontrol.force_stop()
            print('An error occured.')
    finally:
        mywin = visual.Window([1600,900], monitor="testMonitor", units="pix", pos = (0,0))

	   
	      

