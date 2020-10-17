import sqlite3
import socket
import threading

PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONECT_MSG = "|disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
arduinos = []
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
                if clientType == "arduino":
                    arduinos.append([conn, addr])
                elif clientType == "python":
                    print("python client")
                    target = conn.recv(HEADER)
                    target = target.decode(FORMAT)
                    print(target)
                    if target.find("|no target|") == -1:
                        print("fuck")
                        targetsFound = 0
                        for i in range(0, len(arduinos)):
                            if target == str(arduinos[i][2]):
                                messageLength = conn.recv(HEADER).decode(FORMAT)
                                message = conn.recv(int(messageLength)).decode(FORMAT)
                                if message == "conecting":
                                    connTarget.append([addr, target[i][2]])
                                    response = f"|connected to {str(target[i][2])}|"
                                    response = response.encode(FORMAT)
                                    responseLength = len(response)
                                    responseLength = str(responseLength).encode(FORMAT)
                                    responseLength += b' ' * (HEADER - len(responseLength))
                                    conn.send(responseLength)
                                    conn.send(response)
                                else:
                                    print(message)
                                targetsFound += 1
                            elif i == len(arduinos) and target == str(arduinos[i][2]) and targetsFound == 0:
                                response = "|target not found|"
                                response = response.encode(FORMAT)
                                responseLength = len(response)
                                responseLength = str(messageLength).encode(FORMAT)
                                responseLength = b' ' * (HEADER - len(messageLength))
                                conn.send(responseLength)
                                conn.send(response)
                    else:
                        print(True)
                        pythonClients.append([conn, addr])
                        connectionsMessage = ""
                        if len(arduinos) > 0:
                            for i in range(0, len(arduinos)):
                                connectionsMessage += str(arduinos[i][1]) + ","
                            connectionsMessage = connectionsMessage.encode(FORMAT)
                            connectionsLength = len(connectionsMessage)
                            connectionsLength = str(connectionsLength).encode(FORMAT)
                            connectionsLength += b' ' * (HEADER - len(connectionsLength))
                        else:
                            connectionsMessage = "|no arduinos|"
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