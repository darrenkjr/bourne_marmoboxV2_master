from psychopy import visual
import marmobox
import marmocontrol
from watcher import mor_drakka

entry = 1
taskname = 'dummy'
session = 1

#creates infinite loop
while entry == 1:
    print('Background display initiated.')
    mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))
    #r = raw_input('Manual Reward? (y/n): ')

    #if r == 'y':
       # marmocontrol.reward()
        #print('Reward delivered.')
    #elif r == 'n':

        # start tracking taskname
    check = mor_drakka(str(taskname))
    animal_ID = raw_input("Enter animal I.D: ")
    taskname = raw_input('Select Task: ')
    session = check.set_value(str(taskname), session)
    print('Checking session',session)
    #delay = raw_input('Set Delay: ')
    limitTrial = int(raw_input('Set amount of trials: '))

    try:
        print('Starting session' + str(session) + ' ...')
        marmobox.run(taskname,mywin,limitTrial,animal_ID,session) #removed delay param
        mywin
        new = raw_input('Start new session? (y/n): ')

        if new == 'n':
            print('Your funeral.  ')
            #exits while condition
            entry = 2
        else:
            #check task name
            entry = 1

    # except:
    #     mywin.close()
    #     marmocontrol.force_stop()
    #     print('An error occured.')

    finally:
        mywin



