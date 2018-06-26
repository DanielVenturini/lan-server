# -*- coding:ISO-8859-1 -*-
import socket
import mimetypes                # mimetypes.guess_type()
from os import path
from methods import Operation
from methods.CommonGatewayInterface import CommonGatewayInterface
from interface import interface

class Response:

    def __init__(self, conn, resourcePath, cookies, query, parent, servers, headerFields):
        self.operation = Operation.Operation(cookies, query, parent)
        self.resourcePath = resourcePath
        self.headerFields = headerFields
        self.cookies = cookies
        self.servers = servers
        self.parent = parent
        self.query = query
        self.conn = conn

    def response200(self, headerFields):
        if (self.parent == '/CGI' or self.resourcePath[self.resourcePath.rfind("."):] == ".dyn"):
            CommonGatewayInterface(self.resourcePath, self.conn, headerFields, self.operation, self.query, self.parent, self.cookies, self.servers)
            return

        size = 512							        # size of bytes to read and send
        if(path.isfile(self.resourcePath) == False):
            self.responseIndex()
            return

        try:
            response = 'HTTP/1.1 200 OK\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Content-Length: ' + str(path.getsize(self.resourcePath)) + '\r\n' +\
            'Content-Type: ' + str(mimetypes.guess_type(self.resourcePath)[0]) + '\r\n' +\
            'Last-Modified: ' + self.operation.lastModified(self.resourcePath, False) + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

            self.conn.sendall(response.encode())
            print("SENDING THE FILE " + self.resourcePath)

            file = open(self.resourcePath, "rb")
            bytesSequence = file.read(size)        	# read only 512 bytes in each loop
            while(bytes.__len__(bytesSequence)):
                self.send(bytesSequence)	        # send the 512 bytes
                bytesSequence = file.read(size)    	# get nexts 512 bytes

        except (IOError, OSError):
            print("FILE NOT FOUND " + self.resourcePath)
            self.response404()

    def response304(self):
        response = 'HTTP/1.1 304 Not Modified\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.send(response)

    def response401(self, realm):
        response = 'HTTP/1.1 401 Unauthorized\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n' +\
            'WWW-Authenticate: Basic realm=' + '\"' + realm + '\"' + '\r\n\r\n'

        self.send(response)

    def response404(self):

        if(self.findInServers() == True):
            return

        response = 'HTTP/1.1 404 Not Found\r\n ' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n' +\
            'Content-Type: text/html\r\n\r\n' +\
            interface.getHeader('404 Not Found','The Resource Path Is Not Found', self.parent) + '\r\n' \
            '   <p>The requested URL ' + self.resourcePath[1:] + ' was not found on this server.</p>\r\n' \
            '   <hr>\r\n' \
            '       <form method="POST" action="/virtual/feedback">\r\n' \
            '           Write a comment to served<br>\r\n' \
            '           <input type="text" name="comment"><br>\r\n' \
            '           Choose a note:<br>\r\n' \
            '           <select name= "value" >\r\n' \
            '               <option value= "0to2" >0-2</option>\r\n' \
            '               <option value= "3to5" >3-5</option>\r\n' \
            '               <option value= "6to8" >6-8</option>\r\n' \
            '               <option value= "9to10" >9-10</option>\r\n' \
            '           </select ><br><br>\r\n' \
            '           <input type="submit" value="Submit">\r\n' \
            '       </form>\r\n' \
            '   <div>' \
            '       Links importantes:<br><br>' \
            '       Telemetria: virtual/telemetria/status.json<br>\r\n' \
            '       Salvando feedback do 404: feedback/<br>\r\n' \
            '       Path com BasicAutentication: photos/.htaccess&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Arquivo com a senha: .htpasswd -> login=Admin;senha=Admin<br>\r\n' \
            '       Arquivo .DYN: file.dyn<br>\r\n' \
            '       Arquivo CGI: CGI/CGIexecutable<br>\r\n' \
            '   </div>' +\
            interface.getTail()

        self.send(response)

    def response412(self):
        response = 'HTTP/1.1 412 Precondition Failed\r\n '+\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.send(response)

    def responseIndex(self):
        index = self.operation.getIndex(self.resourcePath)

        response = 'HTTP/1.1 200 OK\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Content-Length: ' + str(len(index)) + '\r\n' +\
            'Content-Type: text/html\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n' + index

        self.send(response)

    def send(self, response):
        try:
            if(bytes.__instancecheck__(response)):          # if the response is byte, only send
                self.conn.sendall(response)
            else:
                self.conn.sendall(response.encode())        # else, encode to bytes and send
        except BrokenPipeError:
            print("User Desconected")

    def findInServers(self):

        try:                                                # if the request is from the server, them return without send to another servers
            teste = self.headerFields["FromServer"]
        except KeyError:
            pass
        else:
            return False

        data = self.createRequest()
        toRemove = []                                       # cannot remove the server on the hash in runtime. I may remove after

        for address in self.servers.keys():
            port = int(self.servers[address])
            print("procurando no servidor " + address + " e porta " + str(port))

            resp = self.connectAndGetResponse(address, port, data)
            if(resp == -1):                                     # server not respond
                toRemove.append(address)                        # cannot remove the address of server into a loop
                print("     Servidor nao respondeu")
            elif(resp == 0):                                    # server exists, but not have the request
                print("     Servidor respondeu, mas nao tem o resource")
                continue
            else:                                               # server exists and send the request
                print("     Serviddr respondeu com o resource")
                self.removeAll(toRemove)
                return True

        self.conn.settimeout(None)                              # restore to default
        self.removeAll(toRemove)

        return False

    def connectAndGetResponse(self, ip, port, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create a new socket
        s.settimeout(0.25)                                      # half half second for each server

        try:

            s.connect((ip, port))
            s.send(data.encode())

            response = False
            bytesSequence = s.recv(512)        	            # read only 512 bytes to test the response: 200, 404

            # if the response is 404
            if(self.is404(bytesSequence)):
                return 0

            # the response is not 404. Then send to client
            while(bytes.__len__(bytesSequence)):
                self.conn.send(bytesSequence)	            # send the 512 bytes
                bytesSequence = s.recv(512)    	            # get nexts 512 bytes
                response = True

            if(response):
                return 1
            else:
                return 0

        except (socket.timeout, ConnectionRefusedError):
            return -1
        except BrokenPipeError:
            return 0

    def createRequest(self):
        print("Resorce original: " + self.resourcePath)

        return 'GET ' + self.resourcePath[1:] + ' HTTP/1.1\r\n' +\
                'FromServer: True\r\n\r\n'

    # cannot remove the keys and mapped the hash into a loop. Then, remove now
    def removeAll(self, toRemove):
        for address in toRemove:
            self.servers.pop(address)

    def is404(self, response):
        responseTest = response.decode()
        firstLine = responseTest[:responseTest.index('\n')] # get first line

        # if in first line contains 404
        if(firstLine.find('404') != -1):
            return True
        else:
            return False