

def tasklist(preset):

    if preset == 'y':
        experimental_protocol = input('Enter desired protocol') #enter name of protocol eg: touch training
        full_protocol = 'protocol_exp.'+experimental_protocol
        try:
            tasksuite = importlib.import_module(full_protocol)
        except:
            print('File not found.')

        tasklist = tasksuite.()
        return tasklist

    else:
        task_len = 1
        tasklist = []
        task_len = int(input(('How many different tasks would you like to run')))

        for i in range(task_len):
            task = str(input('Enter task name'))
            tasklist.append(task)

        return tasklist