#Results Relay
import csv
import datetime
import time
class Report:
    def __init__(self,taskname):
        self.startTime = self.timeStamp()
        self.Events = []
        self.filename = './data/'+self.startTime['string'] + str(taskname) + '.csv'
        def createStartEvent():
            self.Events.append({'time':self.startTime,'info':'Start'})
        createStartEvent()

    def timeStamp(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return {'string':st,'seconds':ts}
    def addEvent(self,eventInfo):
        time = self.timeStamp()
        info = eventInfo
        self.Events.append({'time':time,'info':info})
        return
    def save(self):
        with open(self.filename, 'wb') as f:
            reswrite = csv.writer(f, delimiter = ',')
            for item in self.Events:
                if type(item['info'])==dict:
                    info = [item['time']['string'],item['time']['seconds']]
                    for key in item['info']:
                        info.append(key)
                        print key
                        info.append(item['info'][key])
                    reswrite.writerow(info)
                elif type(item['info'])==str:
                    reswrite.writerow([item['time']['string'],item['time']['seconds'],item['info']])
                else:
                    raise Exception('Wrong Type... needs to be dict or string')

