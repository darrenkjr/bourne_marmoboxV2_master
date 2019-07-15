from pymongo import MongoClient

class database_cls:

    def __init__(self):
        print('Database class initiated')
        self.client = MongoClient()

        self.db_animals = self.client['marmobox']
        print(self.db_animals)


    def check_collection(self, animalID):
        #moving into marmoset db, and  checking for existence of animalID database

        self.animalID = animalID
        animalid_db = self.db_animals
        print(self.db_animals.collection_names())

        #check if collection with animalID exists
        self.animal_collection = self.db_animals[animalID]
        print(self.animal_collection)

    def store_in_database(self, results_col, response, trial, session, tasktype):
        # print(response, results_col)
        results = {
            key:value for key, value in zip(results_col,response)
        }
        print(results)
        print('Inserting into mongodb collection: ',self.animal_collection)
        self.animal_collection.insert({'session': session, 'trial': trial, 'task type': tasktype, 'results': results})

    def store_instructions(self, instructions):
        self.instruction_collection = self.db_animals['instructions']
        self.instruction_collection.insert(instructions)

    def evaluate(self):
        print('placeholder')
        #call animalID collection, return list of successes. and pass it
        # animal.