# -*- coding:ISO-8859-1 -*-

from threading import Thread
from methods.GET import GET     # thanks to github@MVGOLOM for help
from methods.POST import POST

class Worker(Thread):

    def __init__(self, conn, addr, data, servers, reqCount, upTime, IP, PORT):
        Thread.__init__(self)

        self.reqCount = reqCount
        self.servers = servers
        self.upTime = upTime
        self.cookies = {}
        self.data = data
        self.conn = conn
        self.PORT = PORT
        self.addr = addr
        self.IP = IP

    def run(self):                          # when starter the thread, this def is execute
        self.data = self.data.decode()
        if(len(self.data) == 0):                 # The Google Chrome sending empty request
            resp = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.conn.sendall(resp.encode())
            return

        print("CONNECTION ADDRESS ", self.addr, end=': ')
        self.readFile()
        self.methods()
        print("Encerrou uma conexao")
        self.conn.close()

    def readFile(self):
        print(self.data[:self.data.index('\r')])
        self.i = 0
        while(self.data[self.i] == '\r' and self.data[self.i+1] == '\n'):   # the protocol allow that the first line in the request be \r\n
            self.i += 2                                                     # so, need ignore this lines

        data = self.data[self.i:]                       # get whitout first '\r\n' lines
        self.msgHTTP = data.split("\r\n")               # splite the data in lines
        line = self.msgHTTP[0].split()                  # get the first line. Ex: GET /file.ext HTTP/1.1
        self.method = line[0]                           # get the Method: GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        self.resourcePath = line[1]                     # get the Path with the Query

        self.resourcePathAndQuery(self.msgHTTP[0])      # separe the Query from the resourcePath
        self.version = line[2]                          # get the version of HTTP

        self.i = 1
        line = self.msgHTTP[self.i].split(': ')         # split the lines in 'key':'value'
        self.headerFields = {}
        while(self.i < len(self.msgHTTP)):

            try:                                        # some browers send the msgHTTP broken
                if(line[0] == "Cookie"):
                    self.setCookies(line[1])
                else:
                    self.headerFields[line[0]] = line[1]

                self.i += 1
                line = self.msgHTTP[self.i].split(': ') # split the lines in 'key':'value'
            except IndexError:
                return

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

    def resourcePathAndQuery(self, line):
        if(self.resourcePath.find('htpasswd') != -1):       # if the request is the file '.htpasswd'. NOT SHOULD return this file
            self.resourcePath = '/'                         # then redirect to root
            self.parent = '/'
            self.query = 'R=N;O=C'
            return

        self.resourcePath = self.resourcePath.split('?')    # split in the Query
        if(len(self.resourcePath) == 2):
            self.query = self.resourcePath[1]
        else:
            #self.query = 'R=N;O=C'                          # R=reference by 'N'ame, 'S'ize, 'L'astModifie; O=Order by 'C'rescent or 'D'ecreasing
            self.query = ''

        self.resourcePath = self.resourcePath[0]            # only the path
        if(self.resourcePath == '/' or self.resourcePath.rindex('/') == 0):
            self.parent = '/'
            return

        self.parent = self.resourcePath[:self.resourcePath.rindex('/')]     # get the parent path
        #if the resource is in CGI but not have '?params'
        try:
            if(self.parent == 'CGI' and line.index('?') == -1):
                self.query = ''
        except ValueError:
            self.query = ''

    def methods(self):
        if(self.method == 'GET'):
            GET(self.resourcePath, self.headerFields, self.conn, self.cookies, self.query, self.parent, self.servers, self.reqCount, self.upTime).getResponse()
        elif(self.method == 'HEAD'):
            pass
        elif(self.method == 'POST'):
            POST(self.resourcePath, self.headerFields, self.conn, self.cookies, self.query, self.parent, self.servers, self.msgHTTP[self.i+1:], self.IP, self.PORT)
        elif(self.method == 'PUT'):
            pass
        elif(self.method == 'DELETE'):
            pass
        elif(self.method == 'TRACE'):
            pass
        elif(self.method == 'CONNECT'):
            pass