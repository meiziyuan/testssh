import paramiko
import time

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
#        for m in cmd:
#            ssh.send(m)
        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = (ssh.recv(2048)).decode()
            buff += str(resp)
        s.close()
        result = buff
    else:
        for m in cmd:
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
    execmd = "echo -e '\
127.0.0.1 localhost \n\
192.168.20.1 wifi.to8to.com \n\
192.168.1.142 mobileapi.to8to.com \n\
192.168.1.142 shapi.to8to.com \n\
192.168.1.142 shimg.to8to.com \n\
192.168.1.142 shpic.to8to.com \n\
192.168.1.142 shstatic.to8to.com \n\
192.168.1.142 shadmin.to8to.com \n\
192.168.1.142 pic.to8to.com \n\
192.168.1.142 img.to8to.com \n\
##auto insert\
    ' >/etc/hosts"
    root_password = 'tgw800_2018'

#    sshclient_execmd(hostname, port, username, password, execmd)
    verification_ssh(hostname,  username, password, port, root_password, execmd)


if __name__ == "__main__":
    main()

