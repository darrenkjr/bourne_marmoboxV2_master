#interface with marmobox, drawing stuff to be sent to marmobox
import importlib
import json
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

    def json_input(self,tasklist,animal_ID):
        #create json file into json_file folder for export to marmobox
        timestamp = datetime.datetime.now()
        print('Creating json and instructions for action by marmobox...')

        #creating dictionary file
        json_input = {'animal_ID':animal_ID, 'tasklist':tasklist
                      }

        json_name = str(timestamp) + '_' + animal_ID

        directory = 'json_files/marmobox_child_input/' + json_name
        self.json_obj = json_obj = json.dumps(json_input)
        return json_obj
        #write to mongodb

    def json_send(self, json_obj):
        print('Sending json with instructions to marmobox. ')
        #send json string to minipc








