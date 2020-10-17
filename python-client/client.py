import socket
import threading

class Client:
    def __init__(self):
        self.HEADER = 64
        self.stdSize = 10
        self.FORMAT = "utf-8"
        self.clientType = "python"
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.DISCONECT_MSG = "|disconnect|"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client.connect(self.ADDR)
    def connect(self):
        clientTypemsg = self.clientType.encode(self.FORMAT)
        clientTypemsgLength = str(len(clientTypemsg)).encode(self.FORMAT)
        clientTypemsgLength += b' ' * (self.HEADER - len(clientTypemsgLength))
        self.client.send(clientTypemsgLength)
        self.client.send(clientTypemsg)
    def getArduinosConnected(self):
        clientTypemsg = self.clientType.encode(self.FORMAT)
        clientTypemsgLength = str(len(clientTypemsg)).encode(self.FORMAT)
        clientTypemsgLength += b' ' * (self.HEADER - len(clientTypemsgLength))
        target = "|no target|"
        target = target.encode(self.FORMAT)
        target += b' ' * (self.HEADER - len(target))

        self.client.send(clientTypemsgLength)
        self.client.send(clientTypemsg)
        self.client.send(target)
        length = self.client.recv(self.HEADER).decode(self.FORMAT)
        print(length)
        arduinos = self.client.recv(int(length)).decode(self.FORMAT)
        arduinos = arduinos.split(",")
        #del arduinos[len(arduinos) - 1]

        return arduinos
    def sendDataToArduino(self, target, data):
        clientTypemsg = self.clientType.encode(self.FORMAT)
        clientTypemsgLength = str(len(clientTypemsg)).encode(self.FORMAT)
        clientTypemsgLength += b' ' * (self.HEADER - len(clientTypemsgLength))
        target = str(target)
        target = target.encode(self.FORMAT)
        targetLength = len(target)
        targetLength = str(targetLength).encode(self.FORMAT)
        targetLength = b'' * (self.HEADER - len(targetLength))
        data = str(data).encode()
        dataLength = str(len(data)).encode(self.FORMAT)

        self.client.send(clientTypemsgLength)
        self.client.send(clientTypemsg)
        self.client.send(targetLength)
        self.client.send(target)
        self.client.send(dataLength)
        self.client.send(data)

        length = self.client.recv(self.HEADER)
        response = self.client.recv(int(length))
        return response