#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.

from protocol_exp.progression_logic import *
from protocol_exp.pseudo_rng import rng_choice
import random


class touchtraining_cls(object):

    def __init__(self):
        print('Touch training protocol import successful. ')

        # defining protocol levels, task name on marmobox child, trial amount and initiating progression instance from progression logic module.

        self.levels = ([cls.__name__ for cls in touchtraining_cls.__subclasses__()]) #checks amount of subclasses (corresponding to available levels in protocol)
        self.taskname = 'tasks.touch-training'
        self.results_col = ['Trial Start', 'X-Position (Pressed)', 'Y-Position (Pressed)',
                                          'Stimulus type','Stimulus Position (Center)',
                                          'Reaction Latency', 'Time held on screen', 'Success (Y/N)', 'Hit', 'Miss', 'Null', 'Valid_Trial', 'Trial End'
                                          ]

        #all interactions with system during touch trainings, are VALID TRIALS
        self.validTrial = True

    def success_logic(self):
        #defining success logic for specific protocol + defining required paramters
        success_framework = int(input('Choose success framework, 1 for global success criteria or 2 for rolling average success. Default = rolling average ' )) or 2
        if success_framework == 1:
            print('Initiating global success progression criterion.')
            self.success_frame = 'global_success'

            #initiating global success class instance
            self.success_instance = global_success()
            self.limitTrial = self.success_instance.input()
            return self.limitTrial, self.success_frame


        elif success_framework == 2:
            print('Initiating rolling average success progression criterion. ')
            self.success_frame = 'rolling_average'

            #initiating rolling avg success instance
            self.success_instance = rolling_avg()
            self.limitTrial = self.success_instance.input()
            return self.limitTrial, self.success_frame


    def success_state(self, success_col):
        #evaluating whether to progress or not and returns pass or fail.

        if self.success_frame == 'global_success':
            #global success criteria - make decision here
            success_state = self.success_instance.global_success_eval(success_col)
            return success_state

        elif self.success_frame == 'rolling_average':
            #rolling average success criteria
            success_state = self.success_instance.rolling_success_eval(success_col)
            return success_state


    def instructions(self):

        self.instruction_list = [level_1.instructions(self),
                                 level_2.instructions(self),
                                 level_3.instructions(self),
                                 level_4.instructions(self)
                                 ]

        return self.instruction_list


class level_1(touchtraining_cls):

    def __init__(self):
        #accessing super class attributes
        super(touchtraining_cls).__init__()

    def instructions(self):

        #level 1, stimuli takes up entire screen, blue stimuli, with stimuli drawn from center
        stim_size = [1280, 720] #entire screen
        color = [-1, -1, 1] #blue
        stim_coord = [0,0] #center
        time_penalty = 0.5  #0.5 for level 1

        #create dictionary to be packaged into json

        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord,
            'ITI for Wrong Response': time_penalty,
            'Valid Trial': self.validTrial
        }

        return instructions

class level_2(touchtraining_cls):

    def __init__(self):
        # accessing super class attributes
        super(touchtraining_cls, self).__init__()

    def instructions(self):

        #level 2, stimuli takes up 700 pixel square, blue stimuli, with stimuli drawn from center
        stim_size = 700  # stim size for 700 pixel square.
        color = [-1, -1, 1]  # blue
        stim_coord = [0, 0]  # center
        time_penalty = 2

        # create dictionary to be packaged into json
        instructions = {
            'Stimulus size': stim_size,
            'Stimulus color': color,
            'Stimulus coordinates': stim_coord,
            'ITI for Wrong Response': time_penalty,
            'Valid Trial': self.validTrial
        }

        return instructions

class level_3(touchtraining_cls):

    def __init__(self):
        # accessing super class attributes
        super(touchtraining_cls, self).__init__()

    def instructions(self):
        # level 3, stimuli further decreases to 550 pixels in size, with pseudo random color choices between red yellow and blue
        stim_size = 550  # entire screen
        stim_coord = [0, 0]  # center
        time_penalty = 2

        color_choices = [[-1, -1, 1], [1, -1, -1], [1, 1, -1]]
        # calling helper pseudo rng function
        choice = rng_choice(len(color_choices), self.limitTrial)
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
            'Stimulus color': color, #is a list of RGB codes for x amount of trials
            'Stimulus coordinates': stim_coord,
            'ITI for Wrong Response': time_penalty,
            'Valid Trial': self.validTrial
        }

        return instructions


class level_4(touchtraining_cls):
    # level 4, random coordinates, smaller size, pseudo random color choices between red yellow and blue

    def __init__(self):
        # accessing super class attributes
        super(touchtraining_cls, self).__init__()

    def instructions(self):
        stim_size = 250 #entire screen
        time_penalty = 2

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
            'Stimulus coordinates': stim_coord,
            'ITI for Wrong Response': time_penalty,
            'Valid Trial': self.validTrial
        }

        return instructions








