# -*- coding:ISO-8859-1 -*-

from Worker import Worker
from Grid import Grid
import network
import socket

class Server:

    def __init__(self, PORT_HTTP, PORT_UNICAST):
        IP, BROADCAST = network.getAddress()    # get the IP and BROADCAST address of this machine based in the 'ifconfig'
        self.BUFFER_SIZE = 2048                 # Normally 1024, but we want fast response
        self.PORT_HTTP = PORT_HTTP
        self.servers = {}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((IP, PORT_HTTP))
        except socket.error:
            self.s.bind((IP, 0))
            PORT_HTTP = self.s.getsockname()[1]

        grid = Grid(IP, PORT_HTTP, PORT_UNICAST, BROADCAST, self.servers)   # create the grid class
        grid.start()                                                            # execute thread

        self.s.listen(5)
        self.running(IP)

    def running(self, IP):

        while True:     # ever on
            print("Wait for new connections on " + IP + ":" + str(self.PORT_HTTP))
            conn, addr = self.s.accept()
            thread = Worker(conn, addr, conn.recv(self.BUFFER_SIZE), self.servers)  # create thread
            thread.start()                                                          # execute thread
            print("Servers: ", self.servers)
            continue

# ----------- END OF CLASS ----------- #

Server(5555, 5554)
