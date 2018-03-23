# -*- coding:ISO-8859-1 -*-

import socket
import threading

class Server:

    def __init__(self, TCP_IP, TCP_PORT):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 512          # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(5)

        self.running()

    def methods(self, data):
        msgHttp = data.split()
        if(msgHttp[0] == 'GET'):
            self.path = '.' + msgHttp[1]
            print("Return the file " + self.path)
            try:
                return 'HTTP/1.1 200 OK\r\n\r\n' + open(self.path, "r").read()
            except IOError:
                print("File not found")
                return "HTTP/1.1 404 Not Found\r\n"
        else:
            return "HTTP/1.1 503 Service Unavailable\r\n"

    def attending(self, conn, addr):
        print("---------Connection address:", addr, "---------")
        data = conn.recv(self.BUFFER_SIZE)
        conn.sendall(self.methods(data))    # echo
        conn.close()

    def running(self):
        print("Running server in " + self.TCP_IP + ":" + str(self.TCP_PORT))
        print("---------Waiting for connection---------")

        while True:     # ever on
            conn, addr = self.s.accept()
            threading.Thread(target = self.attending, args = (conn, addr)).start()
            continue

# ----------- END OF CLASS ----------- #

Server('127.0.0.1', 5555)
