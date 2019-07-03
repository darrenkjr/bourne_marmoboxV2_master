#abstracts marmobox_msater away from both progression logic, and experiemtanl protocol design,
# marmoio links the experiemntal procotol, moarobox master and handles json imports to interface with marmobox child
import importlib
import json
import requests
import datetime


class marmoIO:
    # Configuration Constants:
    marmobox_child_url = 'http://localhost:8000/'

    def __init__(self):
        print('marmoio intitiated. ')

    def tasklist(self,protocol, exp_protocol):
        self.protocol = importlib.import_module(protocol)
        print(self.protocol)
        self.protocol_class = (getattr(self.protocol,exp_protocol))()
        tasklist = self.protocol_class.tasklist_gen()
        return tasklist

    def success_logic(self):
        limitTrial, success_criterion, rolling_sucess_samplesize, success_framework = self.protocol_class.success_logic()
        return limitTrial, success_criterion, rolling_sucess_samplesize, success_framework

    def progression_eval(self):
        success_state = self.protocol.success_state()
        return success_state

    def json_create(self,tasklist,animal_ID, limitTrial):
        #create json file into json_file folder for export to marmobox
        timestamp = datetime.datetime.now()
        print('Creating json and instructions for action by marmobox...')

        #creating dictionary file
        json_input = {'animal_ID':animal_ID, 'tasklist':tasklist, 'Trials' : limitTrial,
                      }

        self.json_obj = json_obj = json.dumps(json_input)
        print(json_obj)
        return json_obj


    def json_send(self, json_obj):
        '''
            Method to send an instruction to the child
        '''
        print('Sending json with instructions to marmobox... ')
        instructions = requests.post(self.marmobox_child_url, json=json_obj)#send json string to minipc and wait for response
        print('Post Request status code: ', instructions.status_code)
        print('Sent instructions: ', instructions.body)
        print('Sent instructions: ', instructions.text)
        self.__json_receive(response.json()) # Converts response to JSON and calls receive callback
        

    def __json_on_response(self,response):
        '''
            (Private) Method called by json_send after response from child
        '''
        # @DKRAJIT NEEDs TO IMPLEMENT DATABASE STOREAGE
        # @KIERENPINTO proposes:
        # self.protocol.write_event(response)
        print('Reading in json marmobox output')

        success = 'placeholder'
        return success









