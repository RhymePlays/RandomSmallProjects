import requests, time, json

def testIP(ip, timeout):
    try:
        req = requests.get(ip, timeout=timeout)
        return {"ip": ip, "code": req.status_code, "timeout": timeout, "time": time.time()}
    except Exception as e:
        return {"ip": ip, "code": e.__class__.__name__, "timeout": timeout, "time": time.time()}

def start():
    ipList = []

    for i3 in range(0, 11):
        for i4 in range(0, 256):
            returnValue = testIP(f"http://10.10.{i3}.{i4}", 0.5)
            ipList.append(returnValue)

            print(returnValue)

    with open("file.log", "a") as f:
        f.write("\n\n\n"+json.dumps(ipList))
start()
