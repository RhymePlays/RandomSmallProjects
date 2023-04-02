import requests, time, json, threading

# Variables
IPQueueList = []

# Parameters
reqTimeout = 0.5
numberOfThreads = 10
logFileDirectory = "PingedIP.log"

i1List = range(10, 11)
i2List = range(10, 11)
i3List = range(10, 11)
i4List = range(0, 256)

# Functions
def testIP(ip, timeout):
    try:
        req = requests.get(ip, timeout=timeout)
        return {"ip": ip, "code": req.status_code, "timeout": timeout, "time": time.time()}
    except Exception as e:
        return {"ip": ip, "code": e.__class__.__name__, "timeout": timeout, "time": time.time()}

def scannerThread(queueListIndex):
    for ip in IPQueueList[queueListIndex]:
        returnValue = testIP(ip, reqTimeout)

        with open(logFileDirectory, "a") as f: f.write("\n"+json.dumps(returnValue)+",")        
        print(returnValue)

def start():
    # Create Queues 
    for i in range(0, numberOfThreads):
        IPQueueList.append([])

    # Populate Queues
    toWhichQueue=0
    for i1 in i1List:
        for i2 in i2List:
            for i3 in i3List:
                for i4 in i4List:
                    IPQueueList[toWhichQueue].append(f"http://{i1}.{i2}.{i3}.{i4}")

                    if toWhichQueue >= numberOfThreads - 1: toWhichQueue = 0
                    else: toWhichQueue = toWhichQueue + 1

    # Start Threads
    for i in range(0, numberOfThreads):
        thread = threading.Thread(target=scannerThread, args=(i,))
        thread.start()
start()
