#structure
#set criterion.
#require setting of protocol of investigator. Loop through task list whilst sucess criterion is not met.
#this will replace splash.py

import marmobox
import marmocontrol
from psychopy import visual
from watcher import mor_drakka
from splash_slave import slave
import time
from savestate import state

#if statement to check for previous session.

animal_ID = raw_input("Enter animal I.D, press enter/return for 'test' : ") or 'test'

#check animal_ID
state_obj = state(animal_ID)

#setting default arguments
if not state_obj:

    sucess_criterion = raw_input('Set your success criterion, press enter/return for 80%:  ') or 80
    progression_num = raw_input('Set amount of sucessive sucesses required, 3 = default:  ') or 3

    task_number = raw_input('How many tasks would you like to run? Press enter/return for 3') or 3
    task_count = int(task_number)
    tasklist = []

    limitTrial = raw_input('How many trials per task would you like to run, press enter/return for 50: ') or 5

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
    sucess_list = [0,0,0] #enter loop later
    progression = [sucess_criterion]*progression_num

else:
    #unpack everything and continue from before, first unpack taskname index and tasklist
    tasklist = state_obj['tasklist'].values[0]
    index = state_obj['taskindex'].values[0]
    taskname = state_obj['taskname'].values[0]

for index, taskname in enumerate(tasklist):
    # reset sucess
        session = 0
        sucess_list = [0,0,0]

    print('Running task: ', taskname)

    try:
        session = state_obj['session'].values[0]
        sucess_list = state_obj['sucess state'].values[0]

    except:
        pass


    while sum(sucess_list) < sum(progression):
        # session counter
        entry = 1
        sucess, session = slave(entry, taskname, session, animal_ID, limitTrial)
        sucess_list.insert(0,sucess)
        del sucess_list[-1]
        print('Sucess rate reached % : ',sucess)
        print('Last 3 sucess rates: ', sucess_list)
        time.sleep(1)

        #save current state: tasklist, taskname, session, animal_ID. limitTrial, sucess list, progression
        state_df
        current_state = state.savestate(state_df)
