#Results Relay
import csv
import datetime
import time
import os
import errno
import pandas as pd

class Report:
    def __init__(self,taskname,animal_ID,event_col,report_type):
        self.startTime = self.timeStamp()
        self.Events = []
        self.dir = 'a'
        #create folder directory
        if report_type == "summary_data":
            self.dir = r'./data' + "/" + str(animal_ID) + "/" + str(taskname) + "/"
        elif report_type == "raw_data":
            self.dir = r'./data'+ "/"+ str(animal_ID) + "/" + str(taskname) + "/" + str(self.st) + "/"

        #set up event_col
        self.event_col = event_col

        return

    def createdir(self):
        #creating csv and creating directory if required.
        if not os.path.exists(os.path.dirname(self.dir)):
            try:
                os.makedirs(os.path.dirname(self.dir))
            except OSError as exc: #Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def data_col(self,taskname):
        ########
        if taskname[:2] == 'RL':
            results_col = ['Session', 'Timestamp', 'Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)',
                           'Reward Stimulus Position', 'Distance from reward center (px)', 'Fixation latency (s)',
                           'Response latency (s)', 'Success (Y/N)', 'Counter']
            summary_col = ['Session', 'Finished Session Time', 'Total Time', 'Trials', 'Hits', 'Misses', 'Timeouts',
                           'Outsides', 'Nulls', 'Average dist from center (Px)', 'Average response latency (s)',
                           'Reward Stimulus - Red', 'Success%']

        elif taskname[:2] == 'to': #fortouchtraining
            results_col = ['Session', 'Timestamp', 'Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)',
                           'Stimulus type', 'Stimulus Position (Center)', 'Distance from center (px)', 'Reaction time',
                           'Success (Y/N)']
            summary_col = ['Session', 'Timestamp (End)', 'Minutes', 'Seconds', 'Trials', 'Hits', 'Misses',
                           'Average dist from center (Px)', 'Average reaction time (s)', 'Success%']

        elif taskname[:2] == 'mo':
            results_col = ['Session', 'Timestamp', 'Trial', 'X-Position (Pressed)', 'Y-Position (Pressed)', 'Time (s)',
                           'Reward Stimulus Position', 'Distance from reward center (px)', 'Fixation latency (s)',
                           'Response latency (s)', 'Success (Y/N)', 'Counter']
            summary_col = ['Session', 'Finished Session Time', 'Total Time', 'Trials', 'Hits', 'Misses', 'Timeouts',
                           'Outsides', 'Nulls', 'Average dist from center (Px)', 'Average response latency (s)',
                           'Reward Stimulus - Red', 'Success%']

        return results_col, summary_col



    def timeStamp(self):
        ts = time.time()
        self.st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        tt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        return {'string':self.st,'seconds':ts,'time':tt}

    #generates trial result and corresponding csv
    def addEvent(self,events):
        time = self.timeStamp()
        #appending results - every trial
        self.df_info = pd.DataFrame(events, columns=self.event_col)
        print(self.df_info)
        return


    def writecsv(self,report_type,session):

        print('Reporting sesson: Session',session)

        if session == 1:
            header_bool = 'True'
        else:
            header_bool = None
        self.df_info.to_csv(self.dir + report_type + '.csv', mode='a',header=header_bool)






