#interface with marmobox, drawing stuff to be sent to marmobox
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
        limitTrial, success_criterion, rolling_sucess_samplesize = self.tasksuite.success_logic()
        return limitTrial, success_criterion, rolling_sucess_samplesize





