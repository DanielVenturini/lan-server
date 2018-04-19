# -*- coding:ISO-8859-1 -* -

from threading import Thread
import socket

class Grid(Thread):

    def __init__(self, IP, PORT):
        Thread.__init__(self)
        self.IP = IP
        self.PORT = PORT

        msgSD = 'SD' + PORT + ' ' + str(8080) + '\n'

        self.dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # create the socket datagram -> SOCK_DGRAM
        self.dgramSocket.sendto(msgSD.encode(), ('172.16.0.63', 5554))          # send the packet to broadcast

        self.servers = {}

    def hear(self):

        while(True):
            data = dgramSocket.recv(20)
            if(data.startswith('AD') == False):
                continue
            else:
                pass
"""
dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dgramSocket.bind(('172.16.0.11', 5554))
dgramSocket.settimeout(5)
(b'brasil', ('172.16.0.11', 57962))
"""