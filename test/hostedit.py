import paramiko
import time

host800 = "127.0.0.1 localhost\\n" \
          "192.168.20.1 wifi.to8to.com\\n"

host_online = "127.0.0.1 localhost\\n" \
              "192.168.20.1 wifi.to8to.com\\n" \
              "192.168.1.221 shadmin.to8to.com\\n" \
              "192.168.1.221 boss.we.com\\n"

hosts_142 = "#142环境配置\\n" \
            "127.0.0.1 localhost\\n" \
            "192.168.20.1 wifi.to8to.com\\n" \
            "192.168.1.142 shapi.to8to.com\\n" \
            "192.168.1.142 mobileapi.to8to.com\\n" \
            "192.168.1.142 pic.to8to.com\\n" \
            "192.168.1.142 shadmin.to8to.com\\n" \
            "192.168.1.142 shimg.to8to.com\\n" \
            "192.168.1.142 shpic.to8to.com\\n" \
            "192.168.1.142 img.to8to.com\\n" \
            "192.168.1.142 boss.we.com\\n"

hosts_172 = "#172环境配置\\n" \
            "127.0.0.1 localhost\\n" \
            "192.168.20.1 wifi.to8to.com\\n" \
            "192.168.1.172 shapi.to8to.com\\n" \
            "192.168.1.172 mobileapi.to8to.com\\n" \
            "192.168.1.172 pic.to8to.com\\n" \
            "192.168.1.172 shadmin.to8to.com\\n" \
            "192.168.1.172 shimg.to8to.com\\n" \
            "192.168.1.172 shpic.to8to.com\\n" \
            "192.168.1.172 img.to8to.com\\n" \
            "192.168.1.142 boss.we.com\\n"
hostname = '192.168.20.1'
port = 3363
username = 'sh_admin'
password = 'to8to_2018'
execmd1 = "echo > /etc/hosts"
###execmd2 = "sed -i '$ a "+hosts_142+"' /etc/hosts"
execmd2 = "echo -e '"+hosts_142+"' > /etc/hosts"
execmd3 ="/etc/init.d/dnsmasq restart"
execmd4 = "cat /etc/hosts"

root_password = 'tgw800_2018'

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

if __name__ == "__main__":
    envir = input("请选择hosts环境(输入编号即可)：\n"
                  "1 142\n"
                  "2 172\n"
                  "3 线上\n"
                  "4 默认\n")
    if (envir == "2"):
        execmd2 = "echo -e '"+hosts_172+"' > /etc/hosts"
    elif(envir == "1"):
        execmd2 = "echo -e '"+hosts_142+"' > /etc/hosts"
    elif(envir == "3"):
        execmd2 = "echo -e '"+host_online+"' > /etc/hosts"
    else:
        execmd2 = "echo -e '"+host800+"' > /etc/hosts"
    verification_ssh(hostname, username, password, port, root_password, execmd1)
    time.sleep(1)
    verification_ssh(hostname, username, password, port, root_password, execmd2)
    verification_ssh(hostname, username, password, port, root_password, execmd3)
    print(verification_ssh(hostname, username, password, port, root_password, execmd4))

