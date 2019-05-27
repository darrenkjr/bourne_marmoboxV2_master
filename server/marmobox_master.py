#controls marmobox and subsequent reward modules

from reports import Report
import importlib
import protocol_exp
from marmoio import marmoIO

results_col = ['test','test']

reportobj_trial = Report('test', 'test', results_col, 'raw_data')
reportobj_trial.createdir()


#control marmobox, prompts for input for task suite.

animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
preset = input('Run a preset experimental protocol or custom suite of tasks? y/n')


tasklist, animalID, limitTrial, success_criterion, rolling_avg_success= marmoIO.tasklist(preset)
print(tasklist,animalID, limitTrial, success_criterion, rolling_avg_success)



#generate report