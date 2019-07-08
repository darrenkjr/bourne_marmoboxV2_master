#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.

from protocol_exp.progression_logic import *
from protocol_exp.pseudo_rng import rng_choice
import random


class touchtraining:

    def __init__(self):
        print('Touch training protocol import successful. ')

        # defining protocol levels, task name on marmobox child, trial amount and initiating progression instance from progression logic module.

        self.levels = len([cls.__name__ for cls in touchtraining.__subclasses__()]) #checks amount of subclasses (corresponding to available levels in protocol)
        self.taskname = 'tasks.touchtraining'

        progression_obj = logic()
        progression_obj.show_logic_types() #checking progression sub classes for available success frameworks
        print('initiating touchtraining protocol classes')

    def show_levels(self):
        levels = [cls.__name__ for cls in touchtraining.__subclasses__()]
        return levels

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

class level_1(touchtraining):

    def __init__(self):
        #accessing super class attributes
        super(touchtraining,self).__init_()

        #level 1, stimuli takes up entire screen, blue stimuli, with stimuli drawn from center
        stim_size = (1280, 720) #entire screen
        color = [-1, -1, 1] #blue
        stim_coord = [0,0] #center

        #create dictionary to be packaged into json

        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord
        }

        return instructions

class level_2(touchtraining):

    def __init__(self):
        # accessing super class attributes
        super(touchtraining, self).__init_()

        #level 2, stimuli takes up 700 pixel square, blue stimuli, with stimuli drawn from center
        stim_size = 700  # stim size for 700 pixel square.
        color = [-1, -1, 1]  # blue
        stim_coord = [0, 0]  # center

        # create dictionary to be packaged into json
        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord
        }

        return instructions

class level_3(touchtraining):

    def __init__(self):
        # accessing super class attributes
        super(touchtraining, self).__init_()

        # level 3, stimuli further decreases to 550 pixels in size, with pseudo random color choices between red yellow and blue
        stim_size = 550  # entire screen
        stim_coord = [0, 0]  # center

        color_choices = [[-1, -1, 1], [1, -1, -1], [1, 1, -1]]
        # calling helper pseudo rng function
        choice = rng_choice(3, self.limitTrial)
        color = []

        for i in range(len(choice)):
            if choice[i] == 0:
                color.append(color_choices[0])
            elif choice[i] == 1:
                color.append(color_choices[1])
            elif choice[i] == 2:
                color.append(color_choices[2])

        # create dictionary to be packaged into json
        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord
        }

        return instructions


class level_4(touchtraining):
    # level 4, random coordinates, smaller size, pseudo random color choices between red yellow and blue

    def __init__(self):
        # accessing super class attributes
        super(touchtraining, self).__init_()

        stim_size = 250 #entire screen

        #pseudo random sampling, given amount of trials required.
        color_choices = [[-1, -1, 1], [1, -1, -1], [1, 1, -1]]
        # calling helper pseudo rng function
        choice = rng_choice(3, self.limitTrial)
        color = []
        rangex = 270
        rangey = 130
        stim_coord = []

        for i in range(len(choice)):
        # returns color choices as a list, for sampling, and generates random coordinates for drawing of stimuli
            if choice[i] == 0:
                color.append(color_choices[0])
            elif choice[i] == 1:
                color.append(color_choices[1])
            elif choice[i] == 2:
                color.append(color_choices[2])

            stim_coord.append([random.uniform(-rangex, rangex), random.uniform(-rangey, rangey)])

        # create dictionary to be packaged into json

        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord
        }

        return instructions











