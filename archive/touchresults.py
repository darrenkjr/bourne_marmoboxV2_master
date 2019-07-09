from psychopy import visual, core, logging, event
import marmocontrol as control
import time

class touch_results:

    #loading in required computations
    def __init__(self,checking, stop, correct,incorrect,touchTimeout,nulls,trial,miss,hits, mywin):


    def motion_coherence(self):
        # count nulls.
        if self.correct is not True and self.incorrect is not True:
            print('Current trial: ', self.trial)
            if not self.touchTimeout:
                print('Touch recorded outside grating')
                core.wait(1)
                self.nulls += 1
                print('Trial: ', self.trial)

        #count miss
        elif self.incorrect == True:
            if not self.touchTimeout:
                print('Miss!')
                self.miss += 1
                self.trial += 1

                self.mywin.flip()
                core.wait(2.0)
                self.checking = True
                self.stop = True

                control.incorrectAnswer()

            else:
                time.sleep(0.01)

        #count hits
        elif self.correct == True:
            if not self.touchTimeout:
                print('Hit!')
                self.hits += 1
                self.trial += 1

                self.mywin.flip()
                core.wait(0.1)
                self.checking = True
                self.stop = True

                control.correctAnswer()

            else:
                time.sleep(0.01)

        return self.nulls,self.miss,self.trial,self.hits, self.checking,self.stop
