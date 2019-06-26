class progression_logic:

    def __init__(self):
        print('loading class sucessful')

    def history_check(self):
        #call SQL list for experiment history - and present marmos

    def show_logic_types(self):
        print('showing available success frameworks:', [cls.__name__ for cls in progression_logic.__subclasses__()])

class rolling_avg(progression_logic):

    def __init__(self):
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
        self.rolling_sucess_samplesize = input('Input sample size to draw sucess rolling average. Default is 100') or 100

        limitTrial, success_criterion, rolling_sucess_samplesize = self.animalID, self.success_criterion, self.rolling_sucess_samplesize
        return limitTrial, success_criterion, rolling_sucess_samplesize

    def rolling_success_status(self, success_criterion, rolling_sucess_samplesize):
    #this success check uses a rolling average
        #call sql success list

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