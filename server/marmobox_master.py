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
        print(taskname + ' found. Total levels / progression detected: ', len(protocol_levels))
    except:
         print('protocol not found. ')


#defining sucess criterion and amount of trials - via marmoio
session = 1

for i in range(len(protocol_levels)):
    #define amount of trials for this specific level.
    limitTrial, success_criterion, rolling_sucess_samplesize, success_framework = marmoio.success_logic()

    #start trial and session counter
    trial = 0

    #run protocol - send http request via marmoio.
    json_obj = marmoio.json_create(taskname,animal_ID)


    while trial <= limitTrial:
        #listen to json response from minipc and send to mongo db.
        marmoio.json_send(json_obj)

        #check success_state, read in mongodb status
        success_state = marmoio.progression_eval()

        trial +=1


    if success_state == False:
        #repeat the task
        i = i - 1
        session += 1
    else:
        #progress to next task (linear), and set session for this new task = 0
        session = 1
        continue




# success_state = marmoIO.