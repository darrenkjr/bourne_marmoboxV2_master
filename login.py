from paramiko import SSHClient, AutoAddPolicy 

def Connect(ip, username='pi', pw='marmoset'):
    print('Connecting to {}@{}...'.format(username, ip))
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(ip, username = username, password = pw)
    print('Connection status =', ssh.get_transport().is_active())
    return ssh

def SendCommand(ssh, command, pw='password'): 

    print('sending a command...', command)
    stdin, stdout, stderr = ssh.exec_command( command )
    if "sudo" in command: 
        stdin.write(pw+'\n')
        stdin.flush()
        print('\nstout:', stdout.read())
        print('\nsterr:', stderr.read())

myssh = Connect(ip='49.127.1.247')
justsendit = SendCommand(myssh, command = 'cd marmobox')   
