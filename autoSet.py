import paramiko
import time

def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.

    print(stdout.read())

    s.close()



def verification_ssh(host,username,password,port,root_pwd,cmd):
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        ssh.send('su - \n')
        buff = ''
        while not buff.endswith('Password: '):
            #python3上一定要调用decode()，将bytes转换为str
            resp = (ssh.recv(9999)).decode()
            buff += resp
        ssh.send(root_pwd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = (ssh.recv(2048)).decode()
            buff += str(resp)
        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = (ssh.recv(2048)).decode()
            buff += str(resp)
        s.close()
        result = buff
    else:
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
    return result

def main():

    hostname = '192.168.20.1'
    port = 3363
    username = 'sh_admin'
    password = 'to8to_2018'
#    execmd = "cat /etc/hosts"
    execmd = "arp"
    root_password = 'tgw800_2018'

#    sshclient_execmd(hostname, port, username, password, execmd)
    verification_ssh(hostname,  username, password, port, root_password, execmd)


if __name__ == "__main__":
    main()
