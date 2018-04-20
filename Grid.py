# -*- coding:ISO-8859-1 -* -

from threading import Thread
import socket

class Grid(Thread):

    def __init__(self, IP, PORT):
        Thread.__init__(self)
        self.IP = IP
        self.PORT = PORT
        self.servers = {}

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # create the socket datagram -> SOCK_DGRAM
        self.TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # create the socket datagram -> SOCK_DGRAM

    def run(self):
        msgSD = 'SD' + self.IP + ' ' + str(5554) + '\n'
        writeUDP(msgSD, self.PORT, self.PORT)               # write in broadcast the SD -> Server Discovery
        hear()

    def hear(self):

        self.UDPSocket.bind(('172.16.1.14', 5554))

        while(True):
            data = dgramSocket.recvfrom(15)                 # receive the 'SD' + númeroPortaRespostaUnicast + ' ' + númeroPortaHTTP + '\n'
            comand = data[0].decode()                       # (b'AD8080\n', ('172.16.1.14', 43525))
            ip = data[1][0]                                 # '172.16.1.14'
            port = data[1][1]                               # 43525

            if(comand.startswith('AD') == True):
                self.processAD(comand, ip, port)
            elif(comand.startswith('SD') == True):
                self.processSD()

    def writeUDP(self, msg, IP, PORT):
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.UDPSocket.sendto(msgSD.encode(), (IP, PORT)) # send the packet to broadcast

    def writeUTF(self, IP, PORT):
        s.connect((IP, PORT))
        data = 'AD' + self.PORT + '\n'
        s.send(data)
        s.close()

    def processAD(self, comand, IP, PORT):
        try:
            self.server[IP] = PORT                          # if not exists, catch the except. If exists, update the port
        except KeyError:
            self.server[IP] = PORT

    def processSD(self):
        pass

"""
dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dgramSocket.bind(('172.16.0.11', 5554))
dgramSocket.settimeout(5)
(b'brasil', ('172.16.0.11', 57962))
"""