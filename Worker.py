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
        data = data.decode()
        if(len(data) == 0):                 # The Google Chrome sending empty request
            resp = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.conn.sendall(resp.encode())
            return

        self.readFile(data)
        self.methods()
        self.conn.close()

    def readFile(self, data):
        print(type(data))
        i = 0
        while(data[i] == '\r' and data[i+1] == '\n'):     # the protocol allow that the first line in the request be \r\n
            i += 2                                        # so, need ignore this lines

        data = data[i:]                         # get whitout first '\r\n' lines
        msgHTTP = data.split("\r\n")            # splite the data in lines
        line = msgHTTP[0].split()               # get the first line. Ex: GET /file.ext HTTP/1.1
        self.method = line[0]                   # get the Method: GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        self.resourcePath = line[1]             # get the Path with the Query

        self.resourcePathAndQuery()             # separe the Query from the resourcePath
        self.version = line[2]                  # get the version of HTTP

        i = 1
        line = msgHTTP[i].split(': ')           # split the lines in 'key':'value'
        self.headerFields = {}
        while(line != ['']):

            if(line[0] == "Cookie"):
                self.setCookies(line[1])
            else:
                self.headerFields[line[0]] = line[1]

            i += 1
            line = msgHTTP[i].split(': ')    # split the lines in 'key':'value'

    def setCookies(self, cookieString):
        cookieString = cookieString.split('; ')
        i = 0
        # sometimes, the Google Chrome send the cookies 'breaked'
        try:
            while(i < len(cookieString)):
                cookiePair = cookieString[i].split("=")
                self.cookies[cookiePair[0]] = cookiePair[1]
                i += 1
        except IndexError:
            return

    def resourcePathAndQuery(self):
        if(self.resourcePath.find('htpasswd') != -1):       # if the request is the file '.htpasswd'. NOT SHOULD return this file
            self.resourcePath = '/'                         # then redirect to root
            self.parent = '/'
            self.query = 'R=N;O=C'
            return

        self.resourcePath = self.resourcePath.split('?')    # split in the Query
        if(len(self.resourcePath) == 2):
            self.query = self.resourcePath[1]
        else:
            self.query = 'R=N;O=C'          # R=reference by 'N'ame, 'S'ize, 'L'astModifie; O=Order by 'C'rescent or 'D'ecreasing

        self.resourcePath = self.resourcePath[0]    # only the path
        if(self.resourcePath == '/' or self.resourcePath.rindex('/') == 0):
            self.parent = '/'
            return

        self.parent = self.resourcePath[:self.resourcePath.rindex('/')]     # get the parent path

    def methods(self):
        if(self.method == 'GET'):
            GET(self.resourcePath, self.headerFields, self.conn, self.cookies, self.query, self.parent).getResponse()
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