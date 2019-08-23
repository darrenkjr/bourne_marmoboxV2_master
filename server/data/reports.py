from datetime import datetime
import pandas as pd
from database_sql import database_cls as sql_database

class reports:

    def __init__(self):
        #initiating database class
        self.database = sql_database()

    def experiment_summary(self, animalID):

        '''Query database given animal ID and produce dataframes before cleaning '''

        commands = (

            '''
            SELECT animals.animal_name, experiment.*, sessions.*, raw_events.* FROM animals, experiment,sessions,raw_events WHERE experiment.experiment_id = 3
            ''' ,
        )

        raw_data = self.database.exec_command(commands)
        df = pd.DataFrame(raw_data)
        print(df)



report = reports()
report.experiment_summary(animalID = 'test')






