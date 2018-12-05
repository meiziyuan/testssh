import paramiko
import time
import testBind.py


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
            buff += resp
        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = (ssh.recv(2048)).decode()
            buff += resp
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
    execmd1 = "/etc/init.d/iotd stop"
    execmd2 = "/etc/init.d/iotd start"
    root_password = 'tgw800_2018'
    for n in range(1, 5):
        print("第",n,"次测试结果：\n")
        if(testBind.data_isNotBind()):
            testBind.test_Bind()
            time.sleep(2)
            testBind.test_Unbind()
            time.sleep(2)
            #停止网关程序
            verification_ssh(hostname,  username, password, port, root_password, execmd1)
            time.sleep(5)
            #重启网关程序
            verification_ssh(hostname, username, password, port, root_password, execmd2)
            time.sleep(10)
        else:
            testBind.test_Unbind()
            time.sleep(2)







if __name__ == "__main__":
    main()
