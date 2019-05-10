#controls marmobox and subsequent reward modules

from reports import Report

results_col = ['test','test']

reportobj_trial = Report('test', 'test', results_col, 'raw_data')
reportobj_trial.createdir()

#control marmobox, prompts for input for task suite.

animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
experimental_protocol = input('Enter experiment logic')


#generate report