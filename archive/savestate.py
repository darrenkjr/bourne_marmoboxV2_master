import pickle
import time
import pandas as pd
import os

#take external parameters and save for next time, loads and asks whether user would like to continue previous session, dependent on animal ID.


class state:
    def __init__(self,animal_ID):
        self.animalID = animal_ID
        # navigate into data folder and search for matching animal_ID
        self.savefile = self.animalID + '.p'
        self.savepath = r'./data' + '/' + self.animalID + '/' + self.savefile


    def loadstate(self):
        #if file == false, then break, else: read in state and display
        if os.path.isfile(self.savepath) == True:
            with open(self.savepath, 'rb') as handle:
                unpacked = pickle.load(handle)
                print('Previous savestate: ', unpacked)
                prev_state = [1]
                return unpacked, prev_state

        else:
            #else, continue with default arguments
            print('No previous session found')
            time.sleep(1.0)
            prev_state = [0]
            unpacked = [0]
            return unpacked, prev_state

    def savestate(self, state_df):
        with open(self.savepath, 'wb') as handle:
            print('saving current state..')
            #reads in current state as dataframe.
            pickle.dump(state_df, handle, protocol = pickle.HIGHEST_PROTOCOL)


    def cleanup(self):
        os.remove(self.savepath)
