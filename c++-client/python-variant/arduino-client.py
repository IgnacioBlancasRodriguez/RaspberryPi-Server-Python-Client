import socket
import threading

class Client:
    def __init__(self):
        self.HEADER = 64
        self.stdSize = 10
        self.FORMAT = "utf-8"
        self.clientType = "arduino"
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
    def loop(self):
        try:
            clientAsking = self.client.recv(self.HEADER).decode(self.FORMAT)
            dataLength = self.client.recv(self.HEADER).decode(self.FORMAT)
            
            return str(dataLength)
        except KeyboardInterrupt:
            return "|keyboard interruption|"
