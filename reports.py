#Results Relay
import csv
import datetime
import time
import os
import errno

class Report:
    def __init__(self,taskname,animal):
        self.startTime = self.timeStamp()
        self.Events = []
        self.dir = r'C:/Users/darre/PycharmProjects/BOURNE_MARMOBOX/data/' +str(taskname) + "/"+ str(animal) + "/" + self.startTime['string'] + '.csv'
        def createStartEvent():
            self.Events.append({'time':self.startTime['time'],'info':'Start'})
        createStartEvent()

    def timeStamp(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        tt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        return {'string':st,'seconds':ts,'time':tt}
    def addEvent(self,eventInfo):
        time = self.timeStamp()
        info = eventInfo
        self.Events.append({'time':str(time['time']),'info':info})
        return
    def save(self):
        if not os.path.exists(os.path.dirname(self.dir)):
            try:
                os.makedirs(os.path.dirname(self.dir))
            except OSError as exc: #Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(self.dir,'w') as f:
            reswrite = csv.writer(f, delimiter = ',')
            for item in self.Events:
                if type(item['info'])==dict:
                    info = [item['time']]
                    for key in item['info']:
                        info.append(key)
                        info.append(item['info'][key])
                    reswrite.writerow(info)
                elif type(item['info'])==str:
                    reswrite.writerow([item['time'],item['info']])
                else:
                    raise Exception('Wrong Type... needs to be dict or string')

