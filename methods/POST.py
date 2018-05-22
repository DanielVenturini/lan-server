# -*- coding: ISO-8859-1 -*-

from methods.Virtual import Virtual
from methods.Response import Response
from interface import interface
from methods.Operation import Operation

class POST:

    def __init__(self, resourcePath, hash, conn, cookies, query, parent, servers, httpBody, IP, PORT):
        self.resourcePath = resourcePath
        self.headerFields = hash
        self.httpBody = httpBody
        self.cookies = cookies
        self.parent = parent
        self.query = query
        self.PORT = PORT
        self.conn = conn
        self.IP = IP

        self.operation = Operation(cookies, query, parent)

        self.response = Response(conn, resourcePath, cookies, query, parent, servers, hash)
        self.execute()

    def execute(self):                              # select the def from the resource

        # if is a resource virtual
        if(self.resourcePath.__contains__("/virtual/")):
            print("Contem virtual")
            Virtual(self).start()                   # is not a thread

            response = 'HTTP/1.1 200 OK\r\n' + \
                       'Server: Venturini/1.1\r\n' + \
                       'Date: ' + self.operation.getCurrentDate() + '\r\n' + \
                       'Content-Type: text/html\r\n' + \
                       'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n' + \
                       interface.getPageFromFeedback('http://'+self.IP+':'+str(self.PORT))

        self.conn.sendall(response.encode())