from configparser import ConfigParser

'''
reads database connection paramters from database.ini file - with user and password. 

'''

def config(filename = 'data/database.ini', section = 'postgresql'):
    #create a parser
    parser = ConfigParser()
    #read config file
    parser.read(filename)

    #create empty dictionary with required credential / parameters
    db = {}
    #denoted in the ini file as [section] in text file
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,filename))

    return db