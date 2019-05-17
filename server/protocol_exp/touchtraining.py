#note relevant task names
#prepare logic flow
#execute and call scripts in marmobox in accordance with logic flow.
#sucess criterion - moving average - determined by querying SQL database.

class touchtraining:

    def __init__(self):
        self.tasklist = ['touch-training0','touchtraining1','touchtraining2','touchtraining3']

        tasklist = self.tasklist

        #send task list to marmobox
        return tasklist


    def sucess_criterion(self):
        #call SQL database.



    def logic(self,sucess):
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

        for tasks in self.tasklist:





