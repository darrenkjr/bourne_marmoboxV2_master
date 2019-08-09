from data.database_sql import database_cls as database

class rolling_avg:

    def __init__(self):

        print('loading class successful')
        self.success_samplesize = 'placeholder'
        self.success_criterion = 'placeholder1'

    def input(self):
        # max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trial per session.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        # this assumes using rolling average success criterion

        self.success_criterion = input('Input sucess criterion % Integer only. Default is 80') or 80
        self.success_samplesize = input('Input sample size to draw sucess rolling average. Default is 100') or 100


        print('Initaiting rolling average framework.')

        return self.limitTrial

    def rolling_success_eval(self, success):

        print('Evaluating success state for rolling averages success frameworks! ')
        #this success check uses a rolling average by calling mongodb success column, assuming that success is binary
        print(success)
        print(len(success))
        success_samplesize = int(self.success_samplesize)
        success_criterion = int(self.success_criterion)

        if len(success) < int(success_samplesize):
            print('Sample size too low. Continue obtaining data')
            success_state = 'placeholder'

        elif len(success) >= int(success_samplesize):
            print('Checking performance so far...')
            #convert success list to percentage
            success_percent = ((sum(success[:success_samplesize]))/success_samplesize) *100
            print(success_percent)

            if success_percent <= success_criterion:
                print('No pass.')
                success_state = False

            elif success_percent >= success_criterion:
                print('Success criterion achieved. Moving on to next task if applicable. ')
                success_state = True

        print(success_state)

        return success_state


class global_success:

    def __init__(self):
        print('Initaiting global success framework! ')

    def input(self):
        # ask for current task parameters, max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trials per session.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        self.success_criterion = input('Input desired success criterion % Integer only. Default is 80 ') or 80
        self.success_samplesize = input('Input required number of sessions required to evaluate performance. Default is 3 ') or 3

        return self.limitTrial

    def global_success_eval(self, success_criterion, success_samplesize, success_col):
        print('Checking global success state. ')

        #this succss check uses a global sucess over multiple sessions of x amount of trials block,
        # ie: 3 consecutive session of over >80% success over 50 trial session blocks. Calls in mongodb column and calculates, and outputs evaluation

