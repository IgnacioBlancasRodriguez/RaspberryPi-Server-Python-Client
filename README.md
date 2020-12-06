# 🖥Client-server-python

This repository contains the code for a litle client-server connection using sockets. The repository contains the code for two types of clients client-server system which you can use to connect your raspberry pi to the internet for you to use in wireless projects which you want to use from anyware.

<hr>

## 🚀Technologies used
This repository uses two main technologies:
 * [Python](https://www.python.org/)
 * [Sockets](https://docs.python.org/3/howto/sockets.html)

<hr>

## 🔧What can it be used for?
The way this code is intended to be uses, is as a packages you add to your projects, or as a base you can expand from, taking in mind that these kind of sockets aren't supported in javascript so if you're planning to use this to create a connection between your javascript web-app and your raspberry pi, this isn't for you.

<hr>

## ⚙How does it work?
Basically, all the socket instancies can send byte encoded messages which each of them can decode and read. Now, going deeper, the communications are structured in what i'd like to call three types of events, client-type, get-arduinos and send-data, each of them consisting of various messages which are always preceded by a standard sized, 64 byte, message containing the length of the next message.

> ### <strong>Sending a client-type event</strong>
> First of all we encode the client-type: 
>```python
> clientTypemsg = self.clientType.encode(self.FORMAT)
> clientTypemsgLength = str(len(clientTypemsg)).encode(self.FORMAT)
> clientTypemsgLength += b' ' * (self.HEADER - len(clientTypemsgLength))
>```
> When that's done we send the client-type:
>```python
> self.client.send(clientTypemsgLength)
> self.client.send(clientTypemsg)
>```

<hr>

> ### <strong>Sending a get-arduinos event</strong>
> To get a list with the connected arduinos you just have to send a target message saying "|no target|", just after sending the client-type message.
> First we create encode the message with the target: 
>```python
> target = "|no target|"
> target = target.encode(self.FORMAT)
> target += b' ' * (self.HEADER - len(target))
>```
> When that's done we send the target:
>```python
> self.client.send(target)
>```
> Then, it's time to recive the array with the raspberrypies connected:
>```python
> length = self.client.recv(self.HEADER).decode(self.FORMAT)
> raspberrypies = self.client.recv(int(length)).decode(self.FORMAT)
> raspberrypies = raspberrypies.split(",")
>
> return arduinos
>```

<hr>

> ### <strong>Sending a send-data event</strong>
> To send data to a raspberry pi you first have to have a target which you can get from the event from before and after that you just send your data after having sent a message with the target you want.
> First we create encode the message with the data: 
>```python
> data = str(data).encode()
> dataLength = str(len(data)).encode(self.FORMAT)
> dataLength += b' ' * (self.HEADER - len(dataLength))
>```
> When that's done we send the data:
>```python
> self.client.send(dataLength)
> self.client.send(data)
>```
> After that, you recive a response message from the server containing the status of your request:
>```python
> length = self.client.recv(self.HEADER).decode(self.FORMAT)
> response = self.client.recv(int(length)).decode(self.FORMAT)
>
> return arduinos
>```