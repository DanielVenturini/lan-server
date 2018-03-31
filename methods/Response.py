# -*- coding:ISO-8859-1 -*-
import mimetypes                # mimetypes.guess_type()
from os import path
from methods import Operation

class Response:

    def __init__(self, conn, resourcePath, cookies):
        self.resourcePath = resourcePath
        self.conn = conn
        self.operation = Operation.Operation(cookies)

    def response200(self):
        size = 256							        # size of bytes to read and send

        try:
            response = 'HTTP/1.1 200 OK\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Content-Length: ' + str(path.getsize(self.resourcePath)) + '\r\n' +\
            'Content-Type: ' + mimetypes.guess_type(self.resourcePath)[0] + '\r\n' +\
            'Last-Modified: ' + self.operation.lastModified(self.resourcePath, False) + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

            self.conn.sendall(response)
            print("SENDING THE FILE " + self.resourcePath)

            file = open(self.resourcePath, "r")
            bytesSequence = file.read(size)        	# read only 128 bytes in each loop
            while(bytesSequence != ""):
                self.conn.sendall(bytesSequence)	# send the 128 bytes
                bytesSequence = file.read(size)    	# get nexts 128 bytes

        except (IOError, OSError):
            print("FILE NOT FOUND " + self.resourcePath)
            self.response404()

    def response304(self):
        response = 'HTTP/1.1 304 Not Modified\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.conn.sendall(response)

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
            '<h1>The Resource Path Is Not Found</h1>' +\
            '<p>The requested URL ' + self.resourcePath[1:] + ' was not found on this server.</p>' +\
            '<hr>' +\
            '<address>Venturini/1.1</address>' +\
            '</body></html>'

        self.conn.sendall(response)

    def response412(self):
        response = 'HTTP/1.1 412 Precondition Failed\r\n '+\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.conn.sendall(response)