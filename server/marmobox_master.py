'''controls marmobox and subsequent reward modules'''


from marmoio import marmoIO as marmoio


results_col = ['test','test']
#initiating marmoio instance
marmoio = marmoio()


#control marmobox, prompts for input for task suite.
print('test')
animal_ID = input("Enter animal I.D, press enter/return for 'test' : ") or 'test'
preset = input('Run a preset experimental protocol or custom suite of tasks? y/n ') or 'y'

#using preset input, determine whether to import custom tasklist or create own protocol
if preset == 'y' or 'Y':
    experimental_protocol = input('Enter desired protocol ')  # enter name of protocol eg: touch training

    #appending to directory structure for importing
    full_protocol = 'protocol_exp.' + experimental_protocol
    print(full_protocol)

    print('Running following protocol' + ' : ' + str(experimental_protocol) + ' on ' + animal_ID + ' ')


    try:
        taskname, protocol_levels = marmoio.protocol_param(full_protocol,experimental_protocol)
        print(taskname + ' found. Total levels / progressions detected: ', protocol_levels)

    except:
        print('protocol not found. ')


#defining sucess criterion and amount of trials - via marmoio
session = 1

for i in range(protocol_levels):
    #define amount of trials for this specific level.
    limitTrial, success_criterion, rolling_sucess_samplesize, success_framework = marmoio.success_logic()

    #defining param for each progression
    protocol_instructions = marmoio.protocol_instructions()

    #start trial and session counter
    trial = 0

    #run protocol - send http request via marmoio.
    #read in task specific paramters, (stim size, color etc.)
    level = i
    instructions = protocol_instructions[i]
    json_obj = marmoio.json_create(taskname,animal_ID,level,instructions)


    while trial <= limitTrial:
        #sends post request to marmobox pc, and retrieve response as result from initating task
        response = marmoio.json_send(json_obj)
        #writing to mongodb

        #query mongodb and determine success_state
        success_state = marmoio.progression_eval()

        trial +=1

    #determinging success_state, if suces_state == True, move to next level, (next class)
    if success_state == False:
        #repeat the task
        i = i - 1
        session += 1
    else:
        #progress to next task (linear), and set session for this new task = 0
        session = 1
        continue




# success_state = marmoIO.