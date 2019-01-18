from psychopy import visual
import marmobox
import marmocontrol

entry = 1

#creates infinite loop
while entry == 1:
    print('Background display initiated.')
    mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
    r = raw_input('Manual Reward? (y/n): ')
    if r == 'y':
        marmocontrol.reward()
        print('Reward delivered.')
    elif r == 'n':
        animal_ID = raw_input("Enter animal I.D: ")
        taskname = raw_input('Select Task: ')
        delay = int(raw_input('Set Delay: '))
        limitTrial = input('Set amount of trials: ')

        try:
            marmobox.run(taskname,delay,mywin,limitTrial,animal_ID)
            mywin.close()
            new = raw_input('Start new session? (y/n): ')
            if new == 'n':
                entry = 2
            else:
                entry = 1
        except:
            mywin.close()
            marmocontrol.force_stop()
            print('An error occured.')
        finally:
            mywin


	   
	      

