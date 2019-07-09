from psychopy import visual
import marmobox
import marmocontrol
from watcher import mor_drakka


def slave(entry,taskname,session,animal_ID,limitTrial):

    #creates infinite loop
    while entry == 1:
        print('Background display initiated.')
        mywin = visual.Window([1280, 720], monitor="testMonitor", units="pix", pos=(0, 0))

        # start tracking taskname
        check = mor_drakka(str(taskname))
        session = check.set_value(str(taskname), session)
        print('Checking session',session)
        #delay = raw_input('Set Delay: ')

        print('Starting session' + str(session) + ' ...')
        sucess,sucesscounter = marmobox.run(taskname,mywin,limitTrial,animal_ID,session) #removed delay param
        mywin.close()

        return sucess, session,sucesscounter



