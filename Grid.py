# -*- coding:ISO-8859-1 -* -

from threading import Thread
import socket

class Grid(Thread):

    def __init__(self, IP, PORT, BROADCAST, servers):
        Thread.__init__(self)
        self.BROADCAST = BROADCAST
        self.PORTUNICAST = 5554
        self.servers = servers
        self.PORT = PORT        # this is my http port
        self.IP = IP

        self.TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create the socket TCP -> SOCK_STREM

    def socketUdpOperations(self):
        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # create the socket datagram -> SOCK_DGRAM
        self.UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)# allow broadcast in the socket

    def run(self):
        # one thread for send and wait in broadcast, and main thread for wait 'AD' packets
        t = Thread(target=self.hearTCP, args=())
        t.setName('TCP')
        t.start()                                                           # wait for 'AD' packets

        self.hearUDP()                                                      # send 'SD' in broadcast and wait for new 'SD'

    def hearUDP(self):
        msgSD = 'SD' + str(self.PORTUNICAST) + ' ' + str(self.PORT) + '\n'  # create a packet 'SD5554 5555\n'

        self.socketUdpOperations()
        self.UDPSocket.sendto(msgSD.encode(), (self.BROADCAST, self.PORTUNICAST))   # send the packet to broadcast

        self.socketUdpOperations()
        self.UDPSocket.bind((self.BROADCAST, self.PORTUNICAST))

        while(True):
            data, addr = self.UDPSocket.recvfrom(15)                         # wait for receive new 'SD'
            print("Aqui no udp data: " , data.decode(), " addr: ", addr)
            self.processData(data, 'UDP', addr)

    def hearTCP(self):

        self.TCPSocket.bind((self.IP, self.PORTUNICAST))
        self.TCPSocket.listen(1)
        self.TCPSocket.settimeout(5)                                    # wait only for 5 seg

        try:

            while(True):
                conn, addr = self.TCPSocket.accept()                        # wait for packet 'AD'
                data = conn.recv(10)                                        # 'AD5555\n'

                self.processData(data, 'TCP', addr)
                conn.close()

        except socket.timeout:
            print('parando de ouvir em TCP')
            return

    def processData(self, data, socketType, address):
        if(socketType == 'UDP'):
            print("Chegou um em broadcast: " + data.decode())
            self.processSD(data, address)
        else:
            print("Chegou uma resposta: " + data.decode())
            self.processAD(data, address)

    def processAD(self, data, address):
        data = data.decode()                        # change the bytes to str -> 'AD5555\n'

        if(data.startswith('AD') == False):
            return

        port = data[2:]
        self.servers[address[0]] = port.replace('\n', '')   # add to the servers hash

    def processSD(self, data, address):
        print("Chegou: " + data.decode())
        comand = data.decode()                      # transform to string -> 'SD5554 5555\n'

        if(comand.startswith('SD') == False):
            return

        ip = address[0]                             # '172.16.1.14'
        portUnicast = comand[2: comand.index(' ')]  # '5554'
        portHttp = comand[comand.index(' ') + 1:-1] # '5555' without the '\n'

        self.servers[ip] = portHttp                 # add the servers
        print("Adicionando a lista de servidores: " + str(ip) + " porta Unicast: " + portUnicast + " porta http: " + portHttp)
        self.writeTCP(ip, int(portUnicast))         # write in the socket the response 'AD5555'

    def writeTCP(self, IP, PORT):
        msg = 'AD' + str(self.PORT) + '\n'
        print("Escrevendo uma resposta: " + msg)
        TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPSocket.settimeout(1)

        try:
            TCPSocket.connect((IP, PORT))               # conect to port unicast of the server
            TCPSocket.sendall(msg.encode())             # send the 'AD5555'
            TCPSocket.close()                           # close the connection
        except socket.timeout:
            print("Excecao de tempo. Nao foi possivel responder um AD para " + IP + ":" + str(PORT))
        except:
            print("Outra excecao")
        else:
            print("Pronto")