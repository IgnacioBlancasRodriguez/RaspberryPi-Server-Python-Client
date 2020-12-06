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
    def getRaspberryPiesConnected(self):
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
        raspberrypies = self.client.recv(int(length)).decode(self.FORMAT)
        raspberrypies = raspberrypies.split(",")

        return raspberrypies
    def sendDataToRaspberryPi(self, target, data):
        clientTypemsg = self.clientType.encode(self.FORMAT)
        clientTypemsgLength = str(len(clientTypemsg)).encode(self.FORMAT)
        clientTypemsgLength += b' ' * (self.HEADER - len(clientTypemsgLength))
        target = str(target)
        print("target:" + str(target))
        target = target.encode(self.FORMAT)
        target += b' ' * (self.HEADER - len(target))
        data = str(data).encode()
        dataLength = str(len(data)).encode(self.FORMAT)
        dataLength += b' ' * (self.HEADER - len(dataLength))

        self.client.send(clientTypemsgLength)
        self.client.send(clientTypemsg)
        self.client.send(target)
        self.client.send(dataLength)
        self.client.send(data)

        length = self.client.recv(self.HEADER).decode(self.FORMAT)
        response = self.client.recv(int(length)).decode(self.FORMAT)
        
        return response