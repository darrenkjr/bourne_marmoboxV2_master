#interface with marmobox.
import importlib

class marmoIO:

    def __init__(self):
        print('Import sucessful. ')

    def tasklist(preset):

        if preset == 'y':
            experimental_protocol = input('Enter desired protocol ') #enter name of protocol eg: touch training
            full_protocol = 'protocol_exp.'+experimental_protocol
            try:
                tasksuite = importlib.import_module(full_protocol)
                tasksuite()
                print(tasksuite)

                tasklist = tasksuite.tasklist_gen()
                print(tasklist)
                animalID, limitTrial, success_criterion, rolling_avg_success = tasksuite.sucess_logic()
                return tasklist,animalID, limitTrial, success_criterion, rolling_avg_success

            except:
                print('File not found.')



        else:
            task_len = 1
            tasklist = []
            task_len = int(input(('How many different tasks would you like to run')))

            for i in range(task_len):
                task = str(input('Enter task name'))
                tasklist.append(task)

            return tasklist

    def success_check(self,success,success_criterion,rolling_avg_success):
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

