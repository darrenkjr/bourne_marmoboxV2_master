
import importlib
import json
import requests
import datetime
import sys
import inspect


'''abstracts marmobox_msater away from both progression logic, and experiemtanl protocol design and links the experimental protocol, marmobox master and handles json imports to interface with the marmobox child pc.'''

class marmoIO:
    # Configuration Constants:
    marmobox_child_url = 'http://127.0.0.1:5000/'

    def __init__(self):
        print('marmoio intitiated. ')

    def protocol_param(self,protocol, exp_protocol):
        self.protocol = importlib.import_module(protocol)
        print(type(self.protocol))

        #access pre-defined protocol attributes
        self.protocol_class = (getattr(self.protocol,exp_protocol+'_cls'))()
        taskname = self.protocol_class.taskname
        levels = self.protocol_class.levels
        #for database purposes
        results_col = self.protocol_class.results_col

        print('showing available levels / progressions :', levels)
        #
        return taskname, len(levels), results_col

    def success_logic(self):
        limitTrial, success_criterion, rolling_sucess_samplesize, success_framework = self.protocol_class.success_logic()
        return limitTrial, success_criterion, rolling_sucess_samplesize, success_framework

    def protocol_instructions(self):
        progress_instructions = self.protocol_class.instructions()
        return progress_instructions

    def progression_eval(self):
        success_state = self.protocol.success_state()
        return success_state

    def json_create(self,taskname,animal_ID,level, protocol_instructions):
        #create json file into json_file folder for export to marmobox
        timestamp = datetime.datetime.now()
        print('Creating json and instructions for action by marmobox...')

        #creating dictionary file
        json_input = {'animal_ID':animal_ID, 'taskname':taskname, 'level': level, 'instructions': protocol_instructions
                      }
        json_obj = json.dumps(json_input)
        print(json_input)
        print(type(json_input))
        return json_obj


    def json_send(self, json_obj):
        '''
            Method to send an instruction to the child
        '''
        print('Sending json with instructions to marmobox... ')
        print(json_obj)
        instructions = requests.post(self.marmobox_child_url, json=json_obj)#send json string to minipc and wait for response
        print('Post Request status code: ', instructions.status_code)
        print('Sent instructions: ', instructions.text)
        self.__json_on_response(instructions.json()) # Converts response to JSON and calls receive callback
        #

    def __json_on_response(self,response):
        '''
            (Private) Method called by json_send after response from child
        '''
        # @DKRAJIT NEEDs TO IMPLEMENT DATABASE STOREAGE
        # @KIERENPINTO proposes:

        print('Reading in json marmobox output')
        marmobox_result = self.protocol.write_event(response)

        return marmobox_result









