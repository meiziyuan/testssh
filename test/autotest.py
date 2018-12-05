import paramiko
import time, random
from test import testBind


hostname = '192.168.20.1'
port = 3363
username = 'sh_admin'
password = 'to8to_2018'
execmd1 = "/etc/init.d/iotd stop"
execmd2 = "/etc/init.d/iotd start"
execmd3 = "netstat | grep 48000"
execmd4 = "ps | grep cloud-client"
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



def test():
    Num = 3000
    NumFail = 0
    NumSuccess = 0
    data = []
    # 重启网关程序
    verification_ssh(hostname, username, password, port, root_password, execmd2)
    isStart()
    for n in range(1, Num+1):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "第", n, "次测试结果:")
        ###如果没连接成功，循环一秒检测连接，连接上云端则跳出循环，绑定网关；60s没连上云端，则跳出整个测试循环，结束测试。
        flag = 0
        for sec in range(1, 60):
            time.sleep(1)
            if (isConnect()):
                flag = 1
                break
        if (flag == 0):
            NumFail = NumFail + 1
            data.append(n)
            break

        if(testBind.test_isNotBind()):
            if(testBind.test_Bind()):
                NumSuccess = NumSuccess + 1
            else:
                NumFail = NumFail + 1
                data.append(n)
                ##绑定失败就跳出当前循环
                break

            time.sleep(2)
            testBind.test_Unbind()
            time.sleep(2)
            #停止网关程序
            verification_ssh(hostname,  username, password, port, root_password, execmd1)
            waitTime = random.randint(5, 10)
            print("时间间隔：", waitTime, "秒")
            isConnect()
            time.sleep(waitTime)
            #重启网关程序
            verification_ssh(hostname, username, password, port, root_password, execmd2)
            isStart()
            print("\n")
        else:
            testBind.test_Unbind()
            NumFail = NumFail + 1
            data.append(n)
            time.sleep(2)

    print("总测试次数：", Num)
    print("成功次数：", NumSuccess)
    print("失败次数", NumFail)
    print("失败在哪些次:", data)

###网关是否连上云端
def isConnect():

    str1 = verification_ssh(hostname, username, password, port, root_password, execmd3)
    print(str1)
    if "ESTABLISHED" in str1:
        print("已成功连接云端")
        return True
    else:
        print("未连接")
        return False

###网关程序是否启动成功
def isStart():
    str = verification_ssh(hostname, username, password, port, root_password, execmd4)
    if "/gateway/cloud-client" in str:
        print("start成功")
        return True
    else:
        print("未启动")
        isStart()
    return

if __name__ == "__main__":
    test()
