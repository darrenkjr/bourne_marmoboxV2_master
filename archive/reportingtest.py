from archive.reports import Report

x = Report('testtask')
x.addEvent('Touch')
x.save()
x.addEvent('NewStimulus')
x.addEvent({'name':'Correct Tap','coordinatesx':1,'coordinatesy':2})
x.save()