#interface with marmobox.
import importlib

class marmoIO:

    def __init__(self):
        print('Import sucessful. ')


    def tasklist(self,protocol):
            self.tasksuite = importlib.import_module(protocol)
            self.tasksuite()
            print(self.tasksuite)

            tasklist = self.tasksuite.tasklist_gen()
            # print(tasklist)
            # animalID, limitTrial, success_criterion, rolling_avg_success = tasksuite.sucess_logic()
            # return tasklist,animalID, limitTrial, success_criterion, rolling_avg_success
            return tasklist

    def success_logic(self):
        limitTrial, success_criterion, rolling_avg_success = self.tasksuite.success_logic()
        return limitTrial, success_criterion, rolling_avg_success

    def success_status(self,success_criterion,rolling_avg_success):
    #this success check uses a rolling average
        #call sql success list

        success = 'placeholder. Call sql list and evaluate'
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



