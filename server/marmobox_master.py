'''controls marmobox and subsequent reward modules'''

from marmoio import marmoIO
from data.database_sql import database_cls as database
import datetime

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


session = 1
for i in range(protocol_levels):
    #define amount of trials for this specific level.

    limitTrial = marmoio.success_logic()

    #defining param for each progression
    protocol_instructions = marmoio.protocol_instructions()

    #start store new experiment in database.

    store_instructions = {'instructions':protocol_instructions}
    experimental_info = [experiment_start, protocol_instructions]

    database.store_instructions(store_instructions)

    #start trial and session counter
    trial = 0

    #run protocol - send http request via marmoio.
    #read in task specific paramters, (stim size, color etc.)
    level = i
    print(protocol_instructions)
    sent_instructions = protocol_instructions[i]
    print(sent_instructions)
    json_obj = marmoio.json_create(taskname,animal_ID,level,sent_instructions)

    #marking start of session, where session refers to X number of trial block for a given progression in a protocol.
    session_start = datetime.datetime.now()
    while trial <= limitTrial:
        #sends post request to marmobox pc, and retrieve response as result from initating task
        response = marmoio.json_send(json_obj)
        #writing results, taskname, level and animal_ID to mongodb
        print(response)
        database.store_in_database(results_col, response, trial, session, taskname+(str(level)))
        #query mongodb and determine success_state
        success_state = marmoio.progression_eval()

        trial +=1

    #determinging success_state, if suces_state == True, move to next level, (next class)
    if success_state == False:
        #repeat the task
        i = i - 1
        session += 1
        session_end = datetime.datetime.now()
    elif success_state == True:
        #progress to next task (linear), and set session for this new task = 0
        session = 1
        session_end = datetime.datetime.now()
        continue

experiment_end = datetime.datetime.now()


# success_state = marmoIO.