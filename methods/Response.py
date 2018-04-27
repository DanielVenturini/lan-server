# -*- coding:ISO-8859-1 -*-
import mimetypes                # mimetypes.guess_type()
from os import path
from methods import Operation
from methods.CommonGatewayInterface import CommonGatewayInterface

class Response:

    def __init__(self, conn, resourcePath, cookies, query, parent, servers):
        self.operation = Operation.Operation(cookies, query, parent)
        self.resourcePath = resourcePath
        self.cookies = cookies
        self.servers = servers
        self.parent = parent
        self.query = query
        self.conn = conn

    def response200(self, headerFields):
        if (self.parent == '/CGI' or self.resourcePath[self.resourcePath.rfind("."):] == ".dyn"):
            CommonGatewayInterface(self.resourcePath, self.conn, headerFields, self.operation, self.query, self.parent, self.cookies)
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
        response = 'HTTP/1.1 404 Not Found\r\n ' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n' +\
            'Content-Type: text/html\r\n\r\n' +\
            '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' +\
            '<html><head>' +\
            '<title>404 Not Found</title>' +\
            '</head><body style="background-color: AliceBlue;">' +\
            '<div style="background-color:yellow">\r\n' +\
            '<hr><h1>The Resource Path Is Not Found</h1><hr>' +\
            '</div><hr>\r\n' +\
            '<p>The requested URL ' + self.resourcePath[1:] + ' was not found on this server.</p>\r\n' +\
            '<table cellspacing="10">\r\n' +\
            '<tr><td><img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4gQBEyAn9IpdbAAAA5pJREFUOMu9lH9sU1UUx7/v3verP7a+dnNhrIrTbZ3QzUUzdVERJf4BOBSN0xiMi8TsD4gY/yDOheg/Jhg1ISYydSQYFCWAGiGoIxRhY2PJgswOuq2zY4xuXelr2WhLu7bvXf94rUbDH1s0nuQk59x7z+fec3POAW4hqzb64Fp/Me91UvxXsrp1/LP2znDU4f7U9a9A7qcvPd/epQZ/vqSx0+M6a3jyw47FxpKVzcN/OvWbRpR12y73v7PTdWjN6pIKSSJgDJCLazY+9fJuecXa30yktk8onO9nDBUN7/0NyBWMps3+91tedG6tvNNkESnAE0CkgECBuVgGBPoCBbsRnFlQewbm/F98F9yDkUdPAECZayuujX1iAJs2+6uqqq2965uXLZN5DoQYkIJKFJB4Q2UBsEhAsQm4Gszgyx/Cwe4zM62D3z7kef0cw8dNHLiWt4O7n2up2E45gBJDBQoI+ReKfB4qGECZ5sGikdloSGPb3vq1q/fAA21xxkDFsi2mdJp/oXy5CSYZIPgLTImRusAblxS+QaTGmqYDiQzhSlbcdv9woE7f8aq7h9rvamOqmmkLBFLUZjOj1EHAU4ByAJ+HJG8avkjzGfCAzAMLGqAmgLhGkMooTd4zfXvpjTSL8lx2FETZMBdnQkTVodhk2G0A4QCOAb5pYGYe8E8zjE0xeAM6pkIMNiuHpMYhFNNxLZxiF73eQ7xVTGKy/7XDk8DJ1Lpf9nGobNZ0naixIjS4BMgW4NzZYDadjF4pVqwWu8OqSKZiUyIr4fyPOZSXEghWHamUxhFOo3ws8FWhcq77fnp8U9j/Ul114/ZjdkftHX1DGswij+nJievdXY81io61mkCzdnNRUYPz3o4PHllTVxOhMrJhhkQix5h+M0f+UegsGvjaO3Dwwaoj+z3tgd9nk45yCkp1AFjIxDzxZKRnKjJx/CiVlAMjvgiCV+MglECWLGDgdP5W7VNa3Zr1n3p2l/8U9p71fL9/fupwAEDK2D3BPfxKpdvpNHfMz2UxdCEM5+02UEqgaxnGLbJFKQANALbsmv2orEx+M6pmcHkiAUWxwHVPKQYHJtPdnXfXkEUCtYJhd4irGGOIJ3JQ7GasdJdgNhRH/7Gd+wCE+KVOojFfUryvsQT19VbojODCeRWeg2/siQe/2QEgt2SgKOFKfD6L4fHh6OjQYK/v9Lufg6knAWSXPCernjgOiLVWoOgZAMvxf8gfuVRj87BbYIEAAAAASUVORK5CYII="></td><td><a href='+self.parent+'>Parent Directory</a></td>\r\n' +\
            '</table>\r\n' +\
            '<hr>' +\
            '<address>Venturini/1.1 -- '+self.operation.getCurrentDate()+'</address>' +\
            '</body></html>'

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