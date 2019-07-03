#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.

from protocol_exp.progression_logic import *


class touchtraining:

    def __init__(self):
        print('Touch training protocol import successful. ')
        progression_obj = logic()
        progression_obj.show_logic_types()
        # print('debugging',progression_obj)
        self.progression_obj = progression_obj
        print('initiating touchtraining protocol classes')

    def tasklist_gen(self):
        #Tasks in order - trial by trial basis
        self.tasklist = ['tasks.touch-training0', 'tasks.touch-training1', 'tasks.touch-training2', 'task.touch-training3']

        tasklist1 = self.tasklist

        # send task list to marmobox - and run
        return tasklist1

    def success_logic(self):
        #defining success logic for specific protocol + defining required paramters
        success_framework = int(input('Choose success framework, 1 for global success criteria or 2 for rolling average success. Default = rolling average ' )) or 2
        if success_framework == 1:
            print('Initiating global success progression criterion.')
            self.success_frame = 1

            #initiating success subclass
            logic()
            global_success()

            #input initial paramters
            limitTrial, success_criterion, success_samplesize = global_success.input(self)
            return limitTrial, success_criterion, success_samplesize


        elif success_framework == 2:
            print('Initiating rolling average success progression criterion. ')
            self.success_frame = 2

            #initiating success subclass
            # initiating success subclass
            logic()
            rolling_avg()

            limitTrial, success_criterion, rolling_sucess_samplesize = rolling_avg.input(self)
            return limitTrial, success_criterion, rolling_sucess_samplesize, success_framework


    def success_state(self,limitTrial, success_criterion, success_samplesize):
        #evaluating whether to progress or not and returns pass or fail.

        if self.success_frame == 1:
            #global success criteria - make decision here
            success_state = self.global_success.global_success_eval(self,limitTrial, success_criterion, success_samplesize)
            return success_state

        elif self.success_frame == 2:
            #rolling average success criteria
            success_state = self.rolling_avg.rolling_success_eval(self,limitTrial, success_criterion, success_samplesize)
            return success_state

    def progression_decision(self, success_state,tasklist):

        #decision making for moving on etc.
        if success_state == True:
            print('Progression criterion satisfied. Proceeding to next task. ')
             #do something
        else:
            print('Progression criterion not satisfied. Repeating task.')
             #do something

















