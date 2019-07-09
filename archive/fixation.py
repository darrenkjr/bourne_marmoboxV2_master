from psychopy import visual
import time, datetime


class fixation:

    def __init__ (self,mywin, taskname, stim_size,mouse,trial,reaction_threshold):
        #draw box and present
        fix_coord = [0, 0]
        centre_box = visual.GratingStim(win=mywin, size=stim_size, pos=fix_coord, color=[-1, -1, -1],
                                        colorSpace='rgb', sf=0)
        self.reaction_threshold = reaction_threshold

        print('checking central fixation')

        centre_box.draw()
        mywin.flip()

        mouse.clickReset()
        fix_start = datetime.datetime.now()

        fixation = False
        print('starting')

        while fixation == False:
            while not mouse.getPressed()[0]:  # checks whether mouse button (i.e. button '0') was pressed
                touchTimeout = False
                time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms
            else:  # If pressed
                xpos = mouse.getPos()[0]  # Returns current positions of mouse during press
                ypos = mouse.getPos()[1]
                fixate_button = mouse.isPressedIn(centre_box)

                if fixate_button == True:
                    if not touchTimeout:
                        print('Hit!')
                        self.time_to_fixate = (datetime.datetime.now() - fix_start).total_seconds()
                        print('Time to fixate (s): ', self.time_to_fixate)

                        trial += 1

                        mywin.flip()
                        touchTimeout = True
                        fixation = True

                    else:
                        time.sleep(0.01)

                if not fixate_button:
                    time.sleep(0.01)



    def timeout(self, reaction_start,session,reward,outsides,t):
        reaction_monitor = (datetime.datetime.now() - reaction_start).total_seconds()
        touch_timeout = False
        if reaction_monitor >= self.reaction_threshold:
            #if timeout exit loops.
            print('Timeout. Back to fixation cue.')
            session_time = datetime.datetime.now().strftime("%H:%M %p")
            append_array = [session, session_time, 'timeout', '', '', time.time() - t, reward, '',
                            '> ' + str(self.reaction_threshold) + ' sec', '', outsides, 'N/A', '']

            timeout = True
            checking2 = True
            return append_array

        else:
            time.sleep(0.01)

    def fixation_time(self):

        fixation_time = self.time_to_fixate

        return fixation_time


            # results.append(append_array)
            # # do not record as trial, reset number
            #
            # reportObj_trial.addEvent(results)
            #
            # core.wait(1)
            # timeouts += 1
            # outsides = 0  # reset outside counter
            # print('Trial: ', trial)
        #     #
        #     # print(trial)
        #     # print(limitTrial)
        #
        # else:
        #     time.sleep(0.01)  # Sleeps if not pressed and then checks again after 10ms - THIS MUST BE ACCOUNTED FOR IF ACCURATELY TIMING RESPONSE LATENCIES
