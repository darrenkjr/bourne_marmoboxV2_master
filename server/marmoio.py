#interface with marmobox.
import importlib
class marmoIO:

    def __init__(self):
        print('Import sucessful. ')

    def tasklist(preset):

        if preset == 'y':
            experimental_protocol = input('Enter desired protocol') #enter name of protocol eg: touch training
            full_protocol = 'protocol_exp.'+experimental_protocol
            try:
                task_module = importlib.import_module(full_protocol)
                print('Import' + full_protocol + ' sucess.')
            except:
                print('File not found.')

            tasklist = task_module.tasklist()
            return tasklist, task_module

        else:
            task_len = 1
            tasklist = []
            task_len = int(input(('How many different tasks would you like to run')))

            for i in range(task_len):
                task = str(input('Enter task name'))
                tasklist.append(task)

            return tasklist

    def sucess_check(self,success,success_criterion,rolling_avg_success):
    #this success check uses a rolling average
        #call success list
        if len(success) < rolling_avg_success:
            print('Sample size too low. Continue obtaining data')

        elif len(success) >= rolling_avg_success:
            print('Checking performance so far...')

            if sum(success[-rolling_avg_success:] <= success_criterion):
                print('No pass.')
                success_state = False

            elif sum(success[-rolling_avg_success:]) >= success_criterion:
                print('Sucess criterion achieved. Moving on to next task if applicable. ')
                success_state = True

        return success_state

