#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.
#sucess criterion - moving average - determined by querying SQL database.
from server.marmoio import marmoIO
print('initiating touchtraining protocol classes')

class touchtraining:

    def __init__(self):
        print('Touch training protocol import successful. ')

    def tasklist_gen(self):
        self.tasklist = ['touch-training0', 'touchtraining1', 'touchtraining2', 'touchtraining3']

        tasklist = self.tasklist

        # send task list to marmobox - and run
        return tasklist

    def success_logic(self):
        #call SQL database for current task parameter
        print('Input protocol parameters...')

        # self.animalID = str(input('Enter animal ID'))

        #max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trial per task.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        #this assumes using rolling average success criterion

        self.success_criterion = input('Input sucess criterion % Integer only. Default is 80') or 80
        self.rolling_avg_sucess = input('Input sample size to draw sucess rolling average. Default is 100') or 100

        limitTrial, success_criterion, rolling_avg_success = self.animalID, self.limitTrial, self.success_criterion, self.rolling_avg_sucess
        return limitTrial, success_criterion, rolling_avg_success


    def progression(self):
        #call sql and marmio, check sucess state and make decision.
        progress_history = []
        limitTrial, success_criterion, rolling_avg_success = marmoIO.success_logic()
        success_state = marmoIO.success_status(success_criterion, rolling_avg_success)

        progress_history.append(success_state)

        if progress_history[-1] == True:
            #progress
        elif:
            #rerun task














