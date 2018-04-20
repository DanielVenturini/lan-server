# -*- coding:ISO-8859-1 -* -

from threading import Thread
import socket

class Grid(Thread):

    def __init__(self, IP, PORT):
        Thread.__init__(self)
        self.IP = IP
        self.PORT = PORT        # this is my http port
        self.BROADCAST = '192.168.0.255'
        self.PORTUNICAST = 5554
        self.servers = {}

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # create the socket datagram -> SOCK_DGRAM
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)# allow broadcast in the socket

        self.TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create the socket TCP -> SOCK_STREM

    def run(self):
        # one thread for send and wait in broadcast, and main thread for wait 'AD' packets
        t = Thread(target=self.hearUDP, args=("void")).start()              # send 'SD' in broadcast and wait for new 'SD'

        self.hearTCP()                                                      # wait for 'AD' packets

    def hearUDP(self, void):
        msgSD = 'SD' + str(self.PORTUNICAST) + ' ' + self.PORT + '\n'       # create a packet 'SD5554 5555\n'

        self.UDPSocket.sendto(msgSD.encode(), (self.BROADCAST, self.PORTUNICAST))   # send the packet to broadcast
        self.UDPSocket.bind((self.IP, self.PORTUNICAST))

        while(True):
            data = self.UDPSocket.recvfrom(15)                              # wait for receive new 'SD'
            self.processData(data, 'UDP', None)

    def hearTCP(self):

        self.TCPSocket.bind((self.IP, self.PORTUNICAST))
        self.TCPSocket.listen(1)

        while(True):
            conn, addr = self.TCPSocket.accept()                        # wait for packet 'AD'
            data = conn.recv(10)                                        # 'AD5555\n'

            self.processData(data, 'TCP', addr)
            conn.close()

    def writeTCP(self, IP, PORT):
        msg = 'AD' + self.PORT + '\n'
        self.TCPSocket.connect((IP, PORT))                  # conect to port unicast of the server
        self.TCPSocket.sendall(msg)                         # send the 'AD5555'
        self.TCPSocket.close()                              # close the connection

    def processData(self, data, socketType, address):
        if(socketType == 'UDP'):
            self.processSD(data)
        else:
            self.processAD(data, address)

    def processAD(self, data, address):
        data = data.decode()                        # change the bytes to str -> 'AD5555\n'

        if(data.startswith('AD') == False):
            return

        port = data[2:]
        self.servers[address] = port                # add to server

    def processSD(self, data):
        comand = data[0].decode()                   # (b'SD5554 5555\n', ('172.16.1.14', 5554))

        if(comand.startswith('SD') == False):
            return

        ip = data[1][0]                             # '172.16.1.14'
        portUnicast = comand[2: comand.index(' ')]  # '5554'
        portHttp = comand[comand.index(' ') + 1:-1] # '5555' without the '\n'

        self.servers[ip] = portHttp                 # add the servers
        self.writeTCP(ip, portUnicast)

