#Results Relay
import csv
import datetime
import time
import os
import errno
import pandas as pd

class Report:
    def __init__(self,taskname,animal_ID,results_col):
        self.startTime = self.timeStamp()
        self.Events = []
        #create folder directory
        self.dir = r'./data/' +str(taskname) + "/"+ str(animal_ID) + "/" + self.startTime['string'] + '.csv'
        #set up results_col
        self.results_col = results_col

        def createStartEvent():
            self.Events.append({'time':self.startTime['time'],'info':'Start'})
        createStartEvent()

    def timeStamp(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        tt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        return {'string':st,'seconds':ts,'time':tt}

    #event defined as a new task result - takes empty dataframe and append
    def addEvent(self,results):
        time = self.timeStamp()
        #appending results
        self.df_info = pd.DataFrame(results, columns=self.results_col)
        print(self.df_info)
        self.df_info.to_csv(self.dir,mode = 'a')
        return

    def save(self):

        #creating csv and creating directory if required.

        if not os.path.exists(os.path.dirname(self.dir)):
            try:
                os.makedirs(os.path.dirname(self.dir))
            except OSError as exc: #Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


        # with open(self.dir,'w') as f:
        #     reswrite = csv.writer(f, delimiter = ',')
        #     for item in self.Events:
        #         if type(item['info'])==dict:
        #             info = [item['time']]
        #             for key in item['info']:
        #                 info.append(key)
        #                 info.append(item['info'][key])
        #             reswrite.writerow(info)
        #         elif type(item['info'])==str:
        #             reswrite.writerow([item['time'],item['info']])
        #         else:
        #             raise Exception('Wrong Type... needs to be dict or string')

