import requests, time, json, threading

# Variables
IPQueueList = []

# Parameters
reqTimeout = 0.5
numberOfThreads = 5

def testIP(ip, timeout):
    try:
        req = requests.get(ip, timeout=timeout)
        return {"ip": ip, "code": req.status_code, "timeout": timeout, "time": time.time()}
    except Exception as e:
        return {"ip": ip, "code": e.__class__.__name__, "timeout": timeout, "time": time.time()}

def scannerThread(queueListIndex):
    for ip in IPQueueList[queueListIndex]:
        returnValue = testIP(ip, reqTimeout)

        with open("file.log", "a") as f: f.write("\n"+json.dumps(returnValue)+",")        
        print(returnValue)

def start():
    # Create Queues 
    for i in range(0, numberOfThreads):
        IPQueueList.append([])

    # Populate Queues
    toWhichQueue=0
    for i1 in range(10, 11):
        for i2 in range(10, 11):
            for i3 in range(10, 11):
                for i4 in range(0, 256):
                    IPQueueList[toWhichQueue].append(f"http://{i1}.{i2}.{i3}.{i4}")

                    if toWhichQueue >= numberOfThreads - 1: toWhichQueue = 0
                    else: toWhichQueue = toWhichQueue + 1

    # Start Threads
    for i in range(0, numberOfThreads):
        thread = threading.Thread(target=scannerThread, args=(i,))
        thread.start()
start()
