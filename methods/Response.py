# -*- coding:ISO-8859-1 -*-
import mimetypes                # mimetypes.guess_type()
from os import path
from methods import Operation

class Response:

    def __init__(self, conn, resourcePath, cookies, query, parent):
        self.resourcePath = resourcePath
        self.conn = conn
        self.parent = parent
        self.operation = Operation.Operation(cookies, query, parent)

    def response200(self):
        size = 256							        # size of bytes to read and send
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
            '<div style="background-color:yellow">\r\n' +\
            '<hr><h1>The Resource Path Is Not Found</h1><hr>' +\
            '</div><hr>\r\n' +\
            '<p>The requested URL ' + self.resourcePath[1:] + ' was not found on this server.</p>\r\n' +\
            '<table cellspacing="10">\r\n' +\
            '<tr><td><img src="/photos/parent-icon.png"></td><td><a href='+self.parent+'>Parent Directory</a></td>\r\n' +\
            '</table>\r\n' +\
            '<hr>' +\
            '<address>Venturini/1.1 -- '+self.operation.getCurrentDate()+'</address>' +\
            '</body></html>'

        self.conn.sendall(response)

    def response412(self):
        response = 'HTTP/1.1 412 Precondition Failed\r\n '+\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.conn.sendall(response)

    def responseIndex(self):
        index = self.operation.getIndex(self.resourcePath)

        response = 'HTTP/1.1 200 OK\r\n' +\
            'Server: Venturini/1.1\r\n' +\
            'Date: ' + self.operation.getCurrentDate() + '\r\n' +\
            'Content-Length: ' + str(len(index)) + '\r\n' +\
            'Content-Type: text/html\r\n' +\
            'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n' + index

        self.conn.sendall(response)