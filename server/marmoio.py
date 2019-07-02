#interface with marmobox, drawing stuff to be sent to marmobox
import importlib
import json
import requests
import datetime


class marmoIO:

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

    def json_input(self,tasklist,animal_ID, limitTrial):
        #create json file into json_file folder for export to marmobox
        timestamp = datetime.datetime.now()
        print('Creating json and instructions for action by marmobox...')

        #creating dictionary file
        json_input = {'animal_ID':animal_ID, 'tasklist':tasklist, 'Trials' : limitTrial,
                      }

        self.json_obj = json_obj = json.dumps(json_input)
        print(json_obj)
        return json_obj
        #write to mongodb

    def json_send(self, json_obj):
        print('Sending json with instructions to marmobox... ')
        url = 'http://localhost:8000/'
        #testing post request url
        instructions = requests.post(url, data = json_obj)
        instructions
        print('Post Request status code: ', instructions.status_code)
        print('Sent instructions: ', instructions.body)

        #send json string to minipc

    def json_receive(self):
        print('Reading in json marmobox output')

        success = 'placeholder'
        return success









