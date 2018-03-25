# -*- coding:ISO-8859-1 -*-

import socket

TCP_IP = '192.168.0.105'
TCP_PORT = 5552
BUFFER_SIZE = 1024
MESSAGE = 'Hello, World!'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = "GET / HTTP 1.1\r\nIf-Modified-Since: Wed, 23 Mar 2018 11:10:50 GMT\r\n\r\n"
s.send(data)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)
