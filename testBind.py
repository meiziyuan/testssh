import requests, time

url = "https://shapi.to8to.com/smartcontrol.php"
headers = {
        "Content-Type": "application/x-www-form-urlencoded"
}

dataBind = {
        "action": "Bind",
        "appid": 61,
        "appostype": 1,
        "appversion": "1.3.0",
        "channel": "应用宝",
        "flag": 1,
        "model": "Gateway",
        "systemversion": "23",
        "to8to_token": "c83e24df",
        "uid": "8430887",
        "version": 2.5,
        "addr": "D4C8B044BEEE"
}

dataUnbind = {
        "action": "Unbind",
        "appid": 61,
        "appostype": 1,
        "appversion": "1.3.0",
        "channel": "应用宝",
        "flag": 1,
        "model": "Gateway",
        "systemversion": "23",
        "to8to_token": "c83e24df",
        "uid": "8430887",
        "version": 2.5,
        "gid": 6298
}

data_isBind = {
        "action": "CheckIsBound",
        "appid": 61,
        "appostype": 1,
        "appversion": "1.3.0",
        "channel": "应用宝",
        "flag": 1,
        "model": "Gateway",
        "systemversion": "23",
        "to8to_token": "c83e24df",
        "uid": "8430887",
        "version": 2.5,
        "mac": "D4C8B044BEEE"
}

def test_isNotBind():
    r = requests.post(url=url, data=data_isBind, headers=headers).json()
    if(r["errorCode"] ==0 and r["data"]["boundStatus"]==1):
        print("网关未绑定！")



def test_Bind():
    r = requests.post(url=url, data=dataBind, headers=headers).json()
    if(r["errorCode"] ==0):
        print("绑定成功！")
    else:
        print("绑定失败！")



def test_Unbind():
    r = requests.post(url=url, data=dataUnbind, headers=headers).json()
    if (r["errorCode"] == 0):
        print("解绑成功！")
    else:
        print("解绑失败！")
if __name__ == "__main__":
    test_Bind()
    time.sleep(2)
    test_Unbind()
