# -*- coding:ISO-8859-1 -*-

from Worker import Worker
import socket

class Server:

    def __init__(self, TCP_IP, TCP_PORT):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 512          # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((TCP_IP, TCP_PORT))
        except socket.error:
            self.s.bind((TCP_IP, 0))
            self.TCP_PORT = self.s.getsockname()[1]

        self.s.listen(5)
        self.running()

    def running(self):

        while True:     # ever on
            print("Wait for new connections on " + self.TCP_IP + ":" + str(self.TCP_PORT))
            conn, addr = self.s.accept()
            thread = Worker(conn, addr, conn.recv(self.BUFFER_SIZE))    # create thread
            thread.start()                                              # execute thread
            continue

# ----------- END OF CLASS ----------- #

Server('192.168.0.105', 5551)
