from psychopy import visual, core, logging, event
import time, random, datetime, math
import numpy as np


def initial_param(mywin):
    mouse = event.Mouse(win=mywin)
    trial = 1
    nulls = 0
    timer = time.time()
    xpos = 0
    ypos = 0
    touchTimeout = False
    correct = []
    wrong = []
    hits = 0
    null = 0
    miss = 0
    results = []
    summary = []

    return mouse, trial,nulls,timer,xpos,ypos, touchTimeout,correct,wrong,hits,null, miss, results, summary

def rng_choice(possible_selection,limitTrial):

    choice = np.repeat([0, possible_selection -1], math.floor(limitTrial / 2))
    if math.floor(limitTrial % 2) > 0:
        choice = np.append(choice, random.randint(0, 1))
    np.random.shuffle(choice)

    return choice



