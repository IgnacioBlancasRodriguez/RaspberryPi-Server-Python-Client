import sqlite3
import socket
import threading

PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONECT_MSG = "|disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
raspberrypies = []
pythonClients = []
connTarget = []
stdSize = 10

def handleClient(conn, addr):
    print(f"New connection: {addr}")

    connected = True
    while connected:
        clientTypeLength = conn.recv(HEADER)
        clientTypeLength = clientTypeLength.decode(FORMAT)
        print(clientTypeLength)
        if clientTypeLength:
            clientType = conn.recv(int(clientTypeLength)).decode(FORMAT)
            #chek the client type
            if clientType:
                if clientType == "raspberrypi":
                    raspberrypies.append([conn, addr])
                    print(raspberrypies)
                elif clientType == "python":
                    print("python client")
                    target = conn.recv(HEADER)
                    target = target.decode(FORMAT)
                    print("target: " + target)
                    if target.find("|no target|") == -1:
                        print("================================================================================")
                        print(f"Target asked: {target}")
                        print("================================================================================")
                        target = target.split(",")
                        targetsFound = 0
                        messageLength = conn.recv(HEADER).decode(FORMAT)
                        message = conn.recv(int(messageLength)).decode(FORMAT)
                        for i in range(0, len(raspberrypies)):
                            if target[0].find(str(raspberrypies[i][1][0])) != -1 and target[1].find(str(raspberrypies[i][1][1])) != -1:
                                if message == "conecting":
                                    connTarget.append([addr, raspberrypies[i][1]])
                                    response = f"|connected to {str(raspberrypies[i][1])}|"
                                    response = response.encode(FORMAT)
                                    responseLength = len(response)
                                    responseLength = str(responseLength).encode(FORMAT)
                                    responseLength += b' ' * (HEADER - len(responseLength))
                                    conn.send(responseLength)
                                    conn.send(response)
                                else:
                                    #|Main sending data to raspberrypi logic|
                                    message = message.encode(FORMAT)
                                    messageLength = messageLength.encode(FORMAT)
                                    
                                    print("================================================================================")
                                    try:
                                        raspberrypies[i][0].send(messageLength)
                                        raspberrypies[i][0].send(message)

                                        response = ("data succesfully sent").encode(FORMAT)
                                        responseLength = str(len(response)).encode(FORMAT)
                                        responseLength += b' ' * (HEADER - len(responseLength))
                                    except Exception:
                                        response = (f"There was an exception: {Exception}").encode(FORMAT)
                                        responseLength = str(len(response)).encode(FORMAT)
                                        responseLength += b' ' * (HEADER - len(responseLength))
                                    conn.send(responseLength)
                                    conn.send(response)
                                    print("Response sent")
                                    print("================================================================================")
                                targetsFound += 1
                        if targetsFound == 0:
                            print("================================================================================")
                            print("Target not found")
                            print("================================================================================")
                            response = "|target not found|"
                            response = response.encode(FORMAT)
                            responseLength = len(response)
                            responseLength = str(responseLength).encode(FORMAT)
                            responseLength += b' ' * (HEADER - len(responseLength))
                            conn.send(responseLength)
                            conn.send(response)
                    else:
                        pythonClients.append([conn, addr])
                        connectionsMessage = ""
                        if len(raspberrypies) > 0:
                            for i in range(0, len(raspberrypies)):
                                connectionsMessage += str(raspberrypies[i][1]) + ","
                            connectionsMessage = connectionsMessage.encode(FORMAT)
                            connectionsLength = len(connectionsMessage)
                            connectionsLength = str(connectionsLength).encode(FORMAT)
                            connectionsLength += b' ' * (HEADER - len(connectionsLength))
                        else:
                            connectionsMessage = "|no raspberrypies|"
                            connectionsMessage = connectionsMessage.encode(FORMAT)
                            connectionsLength = len(connectionsMessage)
                            connectionsLength = str(connectionsLength).encode(FORMAT)
                            connectionsLength += b' ' * (HEADER - len(connectionsLength))
                        print(connectionsLength)
                        conn.send(connectionsLength)
                        conn.send(connectionsMessage)
            else:
                connected = False
    conn.close() 
def start():
    server.listen()
    print("listening...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"Active conections: { threading.activeCount() - 1}")
def clean():
    return

if __name__ == "__main__":
    print("starting...")
    try:
        start()
    except KeyboardInterrupt:
        clean()