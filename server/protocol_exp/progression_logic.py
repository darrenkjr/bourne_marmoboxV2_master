

class progression_logic:

    def __init__(self):
        print('loading class sucessful')

    def rolling_avg(self):
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

        limitTrial, success_criterion, rolling_avg_success = self.animalID, self.success_criterion, self.rolling_avg_sucess
        return limitTrial, success_criterion, rolling_avg_success


    def sustained_perf(self):
        #call sql list over multiple sessions, take session ID, calculate total success over session, over 3 sessions, and display


        #progress from that