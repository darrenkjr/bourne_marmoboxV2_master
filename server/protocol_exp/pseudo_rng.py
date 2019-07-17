import numpy as np
import math
import random
import sys

'''function used to generate pseudo random selection of choices, for equal sampling across all possible choices or possible selection'''

def rng_choice(possible_selection,limitTrial):

    #create logical array
    choice_logical = (np.linspace(0, possible_selection - 1, num=possible_selection))
    choice = np.repeat(choice_logical, math.floor(limitTrial / possible_selection))

    #if not divisible, take remainder or modulo and randomly sample from list of possible selections with reference to remainder.
    remainder = math.floor(limitTrial % possible_selection)

    if remainder > 0:
        for x in range(remainder):
            choice = np.append(choice, random.randint(0, possible_selection-1))

    #check whether length of possible choices is equal to the amount of trials to be run
    try:
        len(choice) == limitTrial
    except:
        print('Length of pseudo random choice array is unequal to amount of trials to be run. Please check pseudo_rng.py')
        sys.exit()

    #randomize choices in logical array
    np.random.shuffle(choice)

    return choice
