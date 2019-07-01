#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.

import protocol_exp.progression_logic as progression_logic
print('initiating touchtraining protocol classes')

class touchtraining:

    def __init__(self):
        print('Touch training protocol import successful. ')

    def tasklist_gen(self):
        self.tasklist = ['touch-training0', 'touchtraining1', 'touchtraining2', 'touchtraining3']

        tasklist1 = self.tasklist

        # send task list to marmobox - and run
        return tasklist1

    def success_logic(self):
        #defining success logic for specific protocol + defining required paramters
        success_framework = (input('Choose success framework, 1 for global success criteria or 2 for rolling average success. Default = rolling average ' )) or 2
        if success_framework == 1:
            print('Initiating global success progression criterion.')

        elif success_framework == 2:
            print('Initiating rolling average success progression criterion. ')
            rolling_avg = progression_logic.rolling_avg()
            limitTrial, success_criterion, rolling_sucess_samplesize = rolling_avg.input()
            return limitTrial, success_criterion, rolling_sucess_samplesize, success_framework


    def success_state(self,limitTrial, success_criterion, rolling_sucess_samplesize):
         success_state = progression_logic.rolling_avg.rolling_success_eval(self,limitTrial, success_criterion, rolling_sucess_samplesize)

         return success_state

    def progression_decision(self, success_state,tasklist):
        if success_state == True:
            print('Progression criterion satisfied. Proceeding to next task. ')
             #d
        else:
            print('Progression criterion not satisfied. Repeating task.')
             #do something

















