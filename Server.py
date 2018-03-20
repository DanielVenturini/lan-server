# -*- coding:ISO-8859-1 -*-

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

response = 'HTTP/1.1 200 OK\r\nHello Brasil!'

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        break
    print "received data:", data
    conn.sendall(response)  # echo

conn.close()

