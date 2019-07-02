class logic:

    def __init__(self):
        print('loading class sucessful')

    def history_check(self):
        print('checking history...')
        #call SQL list for experiment history - and present marmos

    def show_logic_types(self):
        print('showing available success frameworks:', [cls.__name__ for cls in logic.__subclasses__()])

class rolling_avg(logic):

    def __init__(self):
        print('Initaiting rolling average framework.')

    def input(self):
        #call SQL database for current task parameter
        print('Input protocol parameters...')

        #max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trial per session.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        #this assumes using rolling average success criterion

        self.success_criterion = input('Input sucess criterion % Integer only. Default is 80') or 80
        self.rolling_sucess_samplesize = input('Input sample size to draw sucess rolling average. Default is 100') or 100

        limitTrial, success_criterion, rolling_sucess_samplesize = self.limitTrial, self.success_criterion, self.rolling_sucess_samplesize
        return limitTrial, success_criterion, rolling_sucess_samplesize

    def rolling_success_eval(self, success_criterion, rolling_sucess_samplesize):

        print('Evaluating success state for rolling averages success frameworks! ')
        #this success check uses a rolling average by calling mongodb success column, assuming that success is binary

        success = 'call mongo db, read json, placeholder'

        if len(success) < rolling_sucess_samplesize:
            print('Sample size too low. Continue obtaining data')

        elif len(success) >= rolling_sucess_samplesize:
            print('Checking performance so far...')

            if sum(success[-rolling_sucess_samplesize:] <= success_criterion):
                print('No pass.')
                success_state = False

            elif sum(success[-rolling_sucess_samplesize:]) >= success_criterion:
                print('Sucess criterion achieved. Moving on to next task if applicable. ')
                success_state = True

        return success_state


class global_success(logic):

    def __init__(self):
        super(logic,self).__init__()
        print('Initaiting global success framework! ')

    def input(self):
        # ask for current task parameters, max tries to enter trial
        for i in range(5):
            try:
                limitTrial = int(input('Input number of required trials per session.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        success_criterion = input('Input desired success criterion % Integer only. Default is 80 ') or 80
        success_samplesize = input('Input required number of sessions required to evaluate performance. Default is 3 ') or 3

        return limitTrial, success_criterion, success_samplesize

    def global_success_eval(self, limitTrial, success_criterion, success_samplesize):
        print('Checking global success state. ')

        #this succss check uses a global sucess over multiple sessions of x amount of trials block,
        # ie: 3 consecutive session of over >80% success over 50 trial session blocks. Calls in mongodb column and calculates, and outputs evaluation

