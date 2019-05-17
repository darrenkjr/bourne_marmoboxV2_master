#controls marmobox and subsequent reward modules

from reports import Report
import importlib

results_col = ['test','test']

reportobj_trial = Report('test', 'test', results_col, 'raw_data')
reportobj_trial.createdir()

#control marmobox, prompts for input for task suite.

animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
preset = input('Run a preset experimental protocol or custom suite of tasks? y/n')

def tasklist(preset):

    if preset == 'y':
        experimental_protocol = input('Enter desired protocol') #enter name of protocol eg: touch training
        full_protocol = 'protocol_exp.'+experimental_protocol
        try:
            tasksuite = importlib.import_module(full_protocol)
        except:
            print('File not found.')

        tasklist = tasksuite.()
        return tasklist

    else:
        task_len = 1
        tasklist = []
        task_len = int(input(('How many different tasks would you like to run')))

        for i in range(task_len):
            task = str(input('Enter task name'))
            tasklist.append(task)

        return tasklist






#generate report