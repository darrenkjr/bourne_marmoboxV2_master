#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.
#sucess criterion - moving average - determined by querying SQL database.
print('initiating touchtrainig protocol classes')

class touchtraining:

    def __init__(self):
        print('Import class successful. ')

    def tasklist_gen(selfs):
        self.tasklist = ['touch-training0', 'touchtraining1', 'touchtraining2', 'touchtraining3']

        tasklist = self.tasklist

        # send task list to marmobox - and run
        return tasklist
    def sucess_logic(self):
        #call SQL database for current task parameter
        print('Input protocol parameters...')

        self.animalID = str(input('Enter animal ID'))

        #max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trial per task.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        #this assumes using rolling average sucess criterion

        self.success_criterion = input('Input sucess criterion % Integer only.') or 80
        self.rolling_avg_sucess = input('Input sample size to draw sucess rolling average. ') or 100

        animalID, limitTrial, success_criterion, rolling_avg_success = self.animalID, self.limitTrial, self.success_criterion, self.rolling_avg_sucess
        return animalID, limitTrial, success_criterion, rolling_avg_success










