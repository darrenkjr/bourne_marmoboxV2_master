#structure
#set criterion.
#require setting of protocol of investigator. Loop through task list whilst sucess criterion is not met.
#this will replace splash.py


from watcher import mor_drakka
from splash_slave import slave
from savestate import state
import pandas as pd
import numpy as np

#if statement to check for previous session.

animal_ID = raw_input("Enter animal I.D, press enter/return for 'test' : ") or 'test'

#check animal_ID
state_obj = state(animal_ID)
unpacked, prev_state = state_obj.loadstate()
confirm = []

if prev_state[0] == 1:
    #unloading states
    tasklist = unpacked.iloc[0]['tasklist']
    current_task_index = unpacked.iloc[0]['task number']
    current_taskname = unpacked.iloc[0]['current task']
    progression = unpacked.iloc[0]['progression criteria']
    limitTrial = unpacked.iloc[0]['set trials']
    prev_sucess_list = unpacked.iloc[0]['sucess state']
    prev_session = unpacked.iloc[0]['current session']

    confirm = raw_input('Continue from previous session? Y/N: ')

elif prev_state == 0 or confirm == 'n' or 'N':
    try:
        state_obj.cleanup()
        print('cleaning up previous saves..')

    except:
        print('no previous saves detected. Moving on.')
        pass

    sucess_criterion = raw_input('Set your success criterion, press enter/return for 80%:  ') or 80
    progression_num = raw_input('Set amount of sucessive sucesses required, press enter/return for 3  ') or 3

    task_number = raw_input('How many tasks would you like to run? Press enter/return for 3') or 3
    task_count = int(task_number)
    tasklist = []

    limitTrial = raw_input('How many trials per task would you like to run, press enter/return for 50: ') or 50

    while task_number > 0:
        task_suite = raw_input('Input your suite of tasks: ')
        task_number -= 1
        tasklist.append(task_suite)

    print('Confirming test parameters... ')
    print('Global sucess criterion (%): ',sucess_criterion)
    print('Amount of trials per task: ', limitTrial)
    print('Confirming tasks to be run: ', tasklist)
    print('Starting task suite...  ')

    #dummy sucess variable to initiate while loop

    progression = [sucess_criterion]*progression_num
    current_task_index = 0
    current_taskname = 0
    prev_state = False

elif confirm == 'y' or 'Y':
    pass

else:
    pass

sucess_list = [0,0,0] #enter loop later
session = 0
load = 1

print(current_task_index, current_taskname)

try:
    tasklist = tasklist[current_task_index:]
    print(tasklist)
    count = 1
    pass_check_sucess = mor_drakka(count)
    for index,taskname in enumerate(tasklist):

        print('Running saved task: ', taskname)
        sucess_list = [0]



        while np.all(np.array(sucess_list[0:progression_num]) >= progression[0]) == False:
            # session counter
            entry = 1

            #start tracking first pass

            sucess_list = pass_check_sucess.set_pass(count,sucess_list,prev_sucess_list)
            session = pass_check_sucess.set_pass(count,session,prev_session)
            count += 1


            print('current state: ',sucess_list)

            sucess, session = slave(entry, taskname, session, animal_ID, limitTrial)
            session_num = [session]

            print(sucess_list)
            sucess_list.insert(0,sucess)

            print('Sucess rate reached % : ',sucess)
            print('Last 3 sucess rates: ', sucess_list[0:3])
            print('Pass or fail: ', np.all(sucess_list >= progression))

            #save current state: tasklist, taskname, session, animal_ID. limitTrial, sucess list, progression
            saved_dict = {
                'tasklist':[tasklist], 'task number': index, 'current task': taskname, 'progression criteria': [progression], 'set trials': limitTrial, 'current session': session, 'sucess state' :[sucess_list]
            }
            state_df = pd.DataFrame.from_dict(saved_dict)
            current_state = state_obj.savestate(state_df)
            print('current state:' ,state_df)
        count += 1



except:
    for index, taskname in enumerate(tasklist):
        print('Running task: ', taskname)
        sucess_list = [0]

        while np.all(np.array(sucess_list[0:progression_num]) >= progression[0])==False:
            # session counter
            entry = 1
            sucess, session = slave(entry, taskname, session, animal_ID, limitTrial)
            session_num = [session]

            sucess_list.insert(0, sucess)

            print(sucess_list)
            print('Sucess rate reached % : ', sucess)
            print('Last 3 sucess rates: ', sucess_list[0:3])

            # save current state: tasklist, taskname, session, animal_ID. limitTrial, sucess list, progression
            saved_dict = {
                'tasklist': [tasklist], 'task number': index, 'current task': taskname,
                'progression criteria': [progression], 'set trials': limitTrial, 'current session': session,
                'sucess state': [sucess_list]
            }
            state_df = pd.DataFrame.from_dict(saved_dict)
            current_state = state_obj.savestate(state_df)
            print('current state:', state_df)
            print('Pass or fail: ', np.all(sucess_list >= progression))





