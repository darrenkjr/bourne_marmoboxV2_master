import pickle
import time
import pandas as pd
import os

#take external parameters and save for next time, loads and asks whether user would like to continue previous session, dependent on animal ID.


class state:
    def __init_(self,animal_ID):
        self.animal_ID = animal_ID
        # navigate into data folder and search for matching animal_ID
        self.savefile = self.animal_ID + '.p'
        self.savepath = r'./data' + '/' + self.animal_ID + '/' + self.filename

        #if file == false, then break, else: read in state and display
        if os.path.isfile(self.savepath) == True:
            print('Previous session detected. ')
            with open(self.savepath, 'rb') as handle:
                unpacked = pickle.load(handle)
                print('Previous savestate: ', unpacked)
                confirm = raw_input('Continue from last session? Y/N')
                if confirm == 'y' or 'Y':
                    return unpacked
                else:
                    return

        else:
            #else, continue with default arguments
            return

    def savestate(self, state_df):
        with open(self.savepath, 'wb') as handle:
            print('saving current state..')
            #reads in current state as dataframe.
            pickle.dump(state_df, handle, protocol = pickle.HIGHEST_PROTOCOL)
