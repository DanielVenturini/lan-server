# -*- coding:ISO-8859-1 -*-

from threading import Thread
from methods.GET import GET     # thanks to github@MVGOLOM for help

class Worker(Thread):

    def __init__(self, conn, addr):
        print("----- CONNECTION ADDRESS ", addr, " -----")
        self.conn = conn
        self.addr = addr
        self.cookies = {}

    def run(self, data):                    # when starter the thread, this def is execute
        if(len(data) == 0):                 # The Google Chrome sending empty request
            self.conn.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        self.readFile(data)
        self.methods()
        self.conn.close()

    def readFile(self, data):
        print(data)
        i = 0
        while(data[i] == '\r' and data[i+1] == '\n'):     # the protocol allow that the first line in the request be \r\n
            i += 2                                        # so, need ignore this lines

        data = data[i:]                     # get whitout first '\r\n' lines
        msgHTTP = data.split("\r\n")        # splite the data in lines
        line = msgHTTP[0].split()           # get the first line. Ex: GET /file.ext HTTP/1.1
        self.method = line[0]               # get the Method: GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        self.resourcePath = line[1]         # get the Path
        self.version = line[2]              # get the version of HTTP

        i = 0
        self.headerFields = {}
        while(line != ['']):

            if(line[0] == "Cookie"):
                self.getCookies(line[1])
            else:
                self.headerFields[line[0]] = line[1]

            i += 1
            line = msgHTTP[i].split(': ')    # split the lines in 'key':'value'

    def getCookies(cookieString):
        cookieString = cookieString.split('; ')
        i = 0
        while(i < len(cookieString)):
            cookiePair = cookieString[i].split("=")
            self.cookies[cookiePair[0]] = cookiePair[1]
            i += 1

    def methods(self):
        if(self.method == 'GET'):
            GET(self.resourcePath, self.headerFields, self.conn, self.cookies).getFile()
        elif(self.method == 'HEAD'):
            pass
        elif(self.method == 'POST'):
            pass
        elif(self.method == 'PUT'):
            pass
        elif(self.method == 'DELETE'):
            pass
        elif(self.method == 'TRACE'):
            pass
        elif(self.method == 'CONNECT'):
            pass