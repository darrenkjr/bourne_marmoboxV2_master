#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.
#sucess criterion - moving average - determined by querying SQL database.
from server.marmoio import marmoIO
from server.protocol_exp import progression_logic
print('initiating touchtraining protocol classes')

class touchtraining:

    def __init__(self):
        print('Touch training protocol import successful. ')

    def tasklist_gen(self):
        self.tasklist = ['touch-training0', 'touchtraining1', 'touchtraining2', 'touchtraining3']

        tasklist = self.tasklist

        # send task list to marmobox - and run
        return tasklist


    def progression(self):
        #call sql and marmio, check sucess state and make decision.
        progress_history = []
        limitTrial, success_criterion, rolling_sucess_samplesize = progression_logic.rolling_avg()
        success_state = marmoIO.success_status(success_criterion, rolling_sucess_samplesize)

        progress_history.append(success_state)

        if progress_history[-1] == True:
            #progress
        elif:
            #rerun task















