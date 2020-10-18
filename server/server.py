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
clients = []
connTarget = []
stdSize = 10

def handleClient(conn, addr):
    clients.append([conn, addr])
    print(f"New connection: {addr}")

    connected = True
    while connected:
        target = conn.recv(HEADER)
        target = target.decode(FORMAT)
        if target.find("|no target|") == -1:
            targetsFound = 0
            for i in range(0, len(clients)):
                if target == str(clients[i][1]):
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
                        #|Main sending to other client logic|
                        messageLength = messageLength.encode(FORMAT)
                        message = message.encode(FORMAT)
                        
                        try:
                            target[i][0].send(messageLength)
                            target[i][0].send(message)

                            response = "message succesfully sent"
                            response = response.encode(FORMAT)
                            responseLength = len(response)
                            responseLength = str(response).encode(FORMAT)
                            responseLength = b' ' * (HEADER - len(responseLength))
                        except Exception:
                            response = f"an error has ocurred |{str(Exception)}|"
                            response = response.encode(FORMAT)
                            responseLength = len(response)
                            responseLength = str(response).encode(FORMAT)
                            responseLength = b' ' * (HEADER - len(responseLength))
                    targetsFound += 1
                elif i == len(clients) and target == str(clients[i][2]) and targetsFound == 0:
                    response = "|target not found|"
                    response = response.encode(FORMAT)
                    responseLength = len(response)
                    responseLength = str(messageLength).encode(FORMAT)
                    responseLength = b' ' * (HEADER - len(messageLength))
                    conn.send(responseLength)
                    conn.send(response)
        else:
            ClientState = conn.recv(HEADER).decode(FORMAT)
            if ClientState == "|get clients|":
                connectionsMessage = ""
                if len(clients) > 0:
                    for i in range(0, len(clients)):
                        connectionsMessage += str(clients[i][1]) + ","
                    connectionsMessage = connectionsMessage.encode(FORMAT)
                    connectionsLength = len(connectionsMessage)
                    connectionsLength = str(connectionsLength).encode(FORMAT)
                    connectionsLength += b' ' * (HEADER - len(connectionsLength))
                else:
                    connectionsMessage = "|no clients|"
                    connectionsMessage = connectionsMessage.encode(FORMAT)
                    connectionsLength = len(connectionsMessage)
                    connectionsLength = str(connectionsLength).encode(FORMAT)
                    connectionsLength += b' ' * (HEADER - len(connectionsLength))
                print(connectionsLength)
                conn.send(connectionsLength)
                conn.send(connectionsMessage)
            elif ClientState == "|disconnect|":
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