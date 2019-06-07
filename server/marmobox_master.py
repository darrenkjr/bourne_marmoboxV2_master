#controls marmobox and subsequent reward modules

from reports import Report
from marmoio import marmoIO
import datetime

results_col = ['test','test']

reportobj_trial = Report('test', 'test', results_col, 'raw_data')
reportobj_trial.createdir()

#placeholder
#detection of previous trial - pick up where left off? list off previous state, grab from sql database.


#control marmobox, prompts for input for task suite.

animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
preset = input('Run a preset experimental protocol or custom suite of tasks? y/n')

#using preset input, determine whether to import custom tasklist or create own protocol
if preset == 'y' or 'Y':
    experimental_protocol = input('Enter desired protocol ')  # enter name of protocol eg: touch training
    full_protocol = 'protocol_exp.' + experimental_protocol

    try:
        tasklist = marmoIO.tasklist(full_protocol)
    except:
        print('protocol not found.')
else:
    task_len = 1
    tasklist = []
    task_len = int(input(('How many different tasks would you like to run')))

    for i in range(task_len):
        task = str(input('Enter task name'))
        tasklist.append(task)

print('Running following protocol' + ': ' + tasklist + 'on ' + animal_ID)

#post importing tasklist, define sucess criterion
#define sucess criterion
#now defining sucess criterion
limitTrial, success_criterion, rolling_avg_success = marmoIO.success_logic()

#run protocol

#start timer
progression_check_time = datetime.now()
#check sucess rate every x minutes.