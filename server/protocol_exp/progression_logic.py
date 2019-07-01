class progression_logic:

    def __init__(self):
        print('loading class sucessful')

    def history_check(self):
        print('checking history...')
        #call SQL list for experiment history - and present marmos

    def show_logic_types(self):
        print('showing available success frameworks:', [cls.__name__ for cls in progression_logic.__subclasses__()])

class rolling_avg(progression_logic):

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
    #this success check uses a rolling average
        #call sql success lists

        success = 'placeholder. Call sql list and evaluate'
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



class global_sucess(progression_logic):

    def __init__(self):
        print('Input protocol paramters! ')
        # ask for current task parameters
        # max tries to enter trial
        for i in range(5):
            try:
                self.limitTrial = int(input('Input number of required trials per session.'))
            except:
                print('Not a number detected. Be sure to input an integer.')
                continue
            break

        self.success_criterion = input('Input desired success criterion % Integer only. Default is 80 ') or 80
        self.success_samplesize = input('Input required number of sessions required to evaluate performance. Default is 3 ') or 3

        limitTrial, success_criterion, success_samplesize = self.limitTrial, self.success_criterion, self.success_samplesize
        return limitTrial, success_criterion, success_samplesize

    def global_success_eval(self, limitTrial, success_criterion, success_samplesize):
        print('Checking global success state. ')

        #this succss check uses a global sucess over multiple session of x amount of trial block, ie: 3 consecutive session of over >80% success over 50 trial sessions.

