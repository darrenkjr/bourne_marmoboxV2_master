import psycopg2
from config import config
import json
from datetime import datetime

class database_cls:

    def __init__(self):
        ''' connect to PostgreSQL database server '''

        #first set connection to none
        self.connection = None

        try:
            #read in connection paramters from config - database.ini file
            params = config()
            self.connection = psycopg2.connect(**params)
            print('Connecting to marmobox database server...')

            self.cur = self.connection.cursor()
            if self.cur == True:
                print('Connection sucessful. ')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def exit(self):
        print('Exiting database connection.')
        self.cur.close()
        self.connection.close()

    def exec_command(self,commands):
        ''' for executing multiple sql commands at once '''
        try:
            for command in commands:
                print(commands)
                self.cur.execute(command)
                result = self.cur.fetchall()
            self.connection.commit()

            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_tables(self):
        ''' create tables in database '''
        print('executing commands')

        commands = (
            # defining table and table columns and data types
            """
           CREATE TABLE IF NOT EXISTS animals (
            
               animal_id SERIAL PRIMARY KEY, 
               animal_name VARCHAR UNIQUE NOT NULL
               
            )   
            """,
            """
            CREATE TABLE IF NOT EXISTS experiment (
            
                experiment_id SERIAL PRIMARY KEY,
                exp_protocol VARCHAR,
                exp_date TIMESTAMP,   
                progressions VARCHAR,
                success_framework TEXT,
                animal_ID INT REFERENCES animals(animal_id)
               
            )
            """,

            """
            CREATE TABLE IF NOT EXISTS sessions (
            
                session_id SERIAL PRIMARY KEY,
                session_number INT, 
                session_start TIMESTAMP, 
                progression_status VARCHAR,
                session_instructions JSONB,
                trial_number INT, 
                exp_id INT REFERENCES experiment(experiment_id) 
                
            )
            """,


            """
            CREATE TABLE IF NOT EXISTS raw_events (
            
                trial_id SERIAL PRIMARY KEY,
                session_id INT REFERENCES sessions(session_id),
                trial_start TIMESTAMP, 
                results JSONB,
                valid_event BOOLEAN,    
                success INT, 
                trial_end TIMESTAMP 
            )
            """
        )
        return self.__exec_command(commands)

    def check_animal(self,animalid):
        ''' checks records for animal, if doesnt exist, create record in animal table '''

        command = (
            ''' 
            INSERT INTO animals(animal_name) VALUES(%s) on conflict do nothing RETURNING animal_ID; 
        '''
                   )

        self.cur.execute(command,(animalid,))
        self.animal_ID = self.cur.fetchall()
        self.connection.commit()


    def add_newexperiment(self, exp_info):
        ''' cross reference current animal ID and extracts unique animal identified in database and adds new experiment entry into sql database, '''

        exp_protocol, exp_date, progressions, animal_ID = exp_info['protocol'],exp_info['Experiment start'],exp_info['progressions'], exp_info['animal ID']

        unique_animal_query = ''' SELECT animal_ID FROM animals WHERE animal_name = %s '''

        self.cur.execute(unique_animal_query,(animal_ID,))
        self.animal_ID = self.cur.fetchone()[0]
        print(self.animal_ID)

        print('adding new experiment entry')

        insert_experiment_command = (
            """
            INSERT INTO experiment(exp_protocol,exp_date, progressions, animal_ID) VALUES(%s,%s, %s, %s) RETURNING experiment_id;
            
            """
        )

        self.cur.execute(insert_experiment_command,(exp_protocol, exp_date, progressions, self.animal_ID))
        self.exp_id = self.cur.fetchone()[0]
        self.connection.commit()

    def add_session(self, session_info):
        ''' adds new session entry into sql database. Each session entry is associated with a unique experiment ID, linked to a uniqe animal ID. '''
        print('adding new session')

        sess_num, sess_start, progression, sess_instr, trial_num = session_info['session_num'],session_info['session_start'],session_info['progression_status'],session_info['session_instructions'],session_info['trial_num']

        command = (
            """
            INSERT INTO sessions(session_number,session_start,progression_status, session_instructions, trial_number, exp_id) VALUES(%s,%s,%s,%s,%s,%s) RETURNING session_id;
            """
        )

        self.cur.execute(command,(sess_num, sess_start, progression, sess_instr, trial_num, self.exp_id))
        self.session_id = self.cur.fetchone()[0]
        self.connection.commit()

    def new_trial(self, trial_info, results_col):

        ''' adds new events or trials into sql database. Main purpose, to store unstructured data specific to a protocol
        and also extract success state for progression criteria. Each raw event is linked to a unique session id, in turn linked to a unique
         experiment ID and protocol, in turn further linked to a unique animal id. Returns whether the current trial is valid or not.   '''


        #results is read in as dictionary, zipped, and success is read and evaluated as a separate column, results is then converted into
        #json strings and stored
        results = {
            key: value for key, value in zip(results_col, trial_info)
        }

        trial_start, success, trial_end, validTrial = results['Trial Start'], results['Success (Y/N)'], results['Trial End'], results['Valid_Trial']

        # updating raw event table. Results is dumped as a json object.
        result_json = json.dumps(results)

        command = (
            """
            INSERT INTO raw_events(session_id,trial_start,results,success,trial_end, valid_event) VALUES(%s,%s,%s,%s,%s, %s) RETURNING trial_id;

            """
        )

        self.cur.execute(command,(self.session_id,datetime.strptime(trial_start, '%d-%b-%Y %I:%M:%S %p'),result_json,success,datetime.strptime(trial_end,'%d-%b-%Y %I:%M:%S %p'),validTrial))
        self.connection.commit()

        return validTrial

    def extract_success(self):
        ''' Queries success state for current session based on unique session id, and extracts a python success list for examination.
         Does so by calling current unique session ID (self variable) and cross-reference against database.
         '''

        extract_success = (
            '''
            SELECT success FROM raw_events WHERE session_id = %s;
            '''
        )

        self.cur.execute(extract_success,[self.session_id])
        success_list = list(self.cur)
        clean_success_list = list(sum(success_list, ()))

        return clean_success_list

    def load_state(self, animal_name):
        """
        cross_references animalID, pulls latest instruction data, and checks whether previous experiments was incomplete. if so prompt user to either resume or start new
        """

        extract_animalid = (

            '''
            SELECT animal_id FROM animals where animal_name = %s;
            
            '''
        )

        self.cur.execute(extract_animalid, [animal_name])
        unique_id = self.cur.fetchall()

        extract_exp = (

            '''
            SELECT * FROM experiment where animal_id = %s order by exp_date desc limit 1;

            '''
        )

        self.cur.execute(extract_exp,unique_id)

        exp_col = [col[0] for  col  in self.cur.description]
        exp_info = list(self.cur.fetchall()[0])

        exp_id = exp_info[0]

        print(type(exp_id))

        extract_session = (
            '''
            SELECT * FROM sessions where exp_id = %s order by session_start desc limit 1;
            '''
        )
        self.cur.execute(extract_session, [exp_id])

        session_col = [col[0] for col in self.cur.description]
        session_info = list(self.cur.fetchall()[0])

        session_id = session_info[0]

        extract_event = (
            '''
            SELECT * FROM raw_events where session_id = %s order by trial_start desc limit 1;
            '''
        )

        self.cur.execute(extract_event, [session_id])

        event_col = [col[0] for col in self.cur.description]
        event_info = list(self.cur.fetchall()[0])

        #zipping dictionary
        exp_info = dict(zip(exp_col,exp_info))
        session_info = dict(zip(session_col,session_info))
        event_info = dict(zip(event_col, event_info))

        latest_state = {
            'exp_info': exp_info,
            'session_info': session_info,
            'raw_event': event_info
        }

        print('Previous history found.')
        print(latest_state)

        #testing for incompleteness
        print('testing for incompleteness')
        latest_progression = int((latest_state['session_info']['progression_status'])) + 1
        total_progression = int((latest_state['exp_info']['progressions']))

        if total_progression > latest_progression+1:
            print('incomplete experiment detected')

            continue_state = input('Continue from previous incomplete experiment or session ? y/n ') or 'y'

        else:
            print('previous experiment is complete. Proceeding')
            continue_state = 'n'

        return continue_state








