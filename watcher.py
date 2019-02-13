#a simple class, to watch if variables have changed.

class mor_drakka:
    def __init__(self,value):
        self.variable = value

    def set_value(self, new_value,session):
        if self.variable != new_value:
            print('This is a new task!')
            session = 1
            print('Session:', session)
            return session
        else:
            session += 1
            print('Repeating task')

            print('Session:', session)
            return session

    #ensure variable called once only per for loop
    def set_pass(self, new_value, initial_list, unpacked_list):
        if self.variable != new_value:
            print('Current sucess state (new task):', initial_list)
            sucesslist = initial_list
            return initial_list
        else:
            initial_list = unpacked_list
            print('Current sucess state: ', initial_list)
            return initial_list




