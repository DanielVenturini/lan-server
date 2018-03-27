# -*- coding:ISO-8859-1 -*-

from Worker import Worker
import socket

class Server:

    def __init__(self, TCP_IP, TCP_PORT):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 512          # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(5)

        self.running()

    def running(self):
        print("Running server in " + self.TCP_IP + ":" + str(self.TCP_PORT))

        while True:     # ever on
            conn, addr = self.s.accept()
            thread = Worker(conn, addr)             # create thread
            thread.run(conn.recv(self.BUFFER_SIZE)) # execute thread
            continue

# ----------- END OF CLASS ----------- #

Server('127.0.0.1', 5552)
