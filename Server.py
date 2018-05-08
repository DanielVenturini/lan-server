# -*- coding:ISO-8859-1 -*-

from Worker import Worker
from Grid import Grid
import network
import socket

class Server:

    def __init__(self, TCP_PORT):
        TCP_IP, BROADCAST = network.getAddress()      # get the IP and BROADCAST address of this machine based in the 'ifconfig'
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 2048          # Normally 1024, but we want fast response
        self.servers = {}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((TCP_IP, TCP_PORT))
        except socket.error:
            self.s.bind((TCP_IP, 0))
            TCP_PORT = self.s.getsockname()[1]

        grid = Grid(TCP_IP, TCP_PORT, BROADCAST, self.servers)  # create the grid class
        grid.start()                                            # execute thread

        self.s.listen(5)
        self.running(TCP_IP)

    def running(self, TCP_IP):

        while True:     # ever on
            print("Wait for new connections on " + TCP_IP + ":" + str(self.TCP_PORT))
            conn, addr = self.s.accept()
            thread = Worker(conn, addr, conn.recv(self.BUFFER_SIZE), self.servers)  # create thread
            thread.start()                                                          # execute thread
            print("Servers: ", self.servers)
            continue

# ----------- END OF CLASS ----------- #

Server(5555)
