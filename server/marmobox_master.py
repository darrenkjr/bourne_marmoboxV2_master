'''controls marmobox and subsequent reward modules'''

from marmoio import marmoIO
from data.database_sql import database_cls as database
import datetime
import json


results_col = ['test','test']
#initiating marmoio instance
marmoio = marmoIO()
database = database()

#create postgreSQL tables if does not exist, else move on
database.create_tables()

#control marmobox, prompts for input for task suite.
print('test')
animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
preset = input('Run a preset experimental protocol or custom suite of tasks? y/n ') or 'y'

#check for previous collection based on animal_ID, if doesnt exist, insert new row
database.check_animal(animal_ID)

#using preset input, determine whether to import custom tasklist or create own protocol
if preset == 'y' or 'Y':
    experimental_protocol = input('Enter desired protocol ')  # enter name of protocol eg: touch training

    #appending to directory structure for importing
    full_protocol = 'protocol_exp.' + experimental_protocol
    print(full_protocol)

    print('Running following protocol' + ' : ' + str(experimental_protocol) + ' on ' + animal_ID + ' ')

    #
    # try:
    taskname, protocol_levels, results_col = marmoio.protocol_param(full_protocol,experimental_protocol)
    print(taskname + ' found. Total levels / progressions detected: ', protocol_levels)
    print('Collecting following raw parameters: ', results_col)

    # except:
    #     print('protocol not found. ')


#defining sucess criterion and amount of trials - via marmoio. Start new experiment
experiment_start = datetime.datetime.now()

#start session counter
session = 1

limitTrial = marmoio.success_logic()
for i in range(protocol_levels):
    success_state = 'placeholder'
    while success_state is not True:

        #defining param for each progression
        protocol_instructions = marmoio.protocol_instructions()
        #store new experiment info in database as dictionary.
        exp_info = {
            'protocol': experimental_protocol,
            'Experiment start': experiment_start,
            'progressions' : protocol_levels,
            'animal ID' : animal_ID
        }
        database.add_experiment(exp_info)

        #start trial counter
        trial = 0

        #read in task specific paramters, (stim size, color etc.) and generate protocol instructions for marmobox
        level = i
        sent_instructions = protocol_instructions[i]

        #start new session and send to database as dictionary
        #check for list of list in dictionary, if so iterate through lists of lists.
        print('Sent intructions:',sent_instructions)


        #marking start of session, where session refers to X number of trial block for a given progression in a protocol.
        session_start = datetime.datetime.now()

        session_info = {
            'session_num': session,
            'session_start': session_start,
            'progression_status': level,
            'session_instructions': json.dumps(sent_instructions),
            'trial_num': limitTrial,
        }

        database.add_session(session_info)

        validTrial = 0

        while validTrial <= limitTrial:
            json_obj = marmoio.json_create(taskname, animal_ID, level, sent_instructions,validTrial)
            #sends post request to marmobox pc, and retrieve response as result from initating task
            response = marmoio.json_send(json_obj)
            #writing results, taskname, level and animal_ID to mongodb
            print(response)
            valid = database.new_trial(response,results_col)
            #query mongodb and determine success_state
            success_col = database.extract_success()
            success_state = marmoio.progression_eval(success_col)

            if valid is True:
                validTrial += 1

            # determinging success_state, if suces_state == True, move to next level, (next class)
            if success_state == True:
                session = 1
                break

        if success_state == False:
            #repeat the task
            print('Repeating task as new session')
            session += 1
            session_end = datetime.datetime.now()

experiment_end = datetime.datetime.now()


# success_state = marmoIO.