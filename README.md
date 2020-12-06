# 🖥Client-server-python

This repository contains the code for a litle client-server connection using sockets. The repository contains to branches, the main one, in which we only have one type of client, and the python-raspberry-pi branch, which contains the code for two types of clients, the base client, and the raspberry pi client.

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
> When that's done it sends the client-type:
>```python
> self.client.send(clientTypemsgLength)
> self.client.send(clientTypemsg)
>```