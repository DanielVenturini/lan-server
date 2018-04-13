# -*- coding: ISO-8859-1 -*-
from os import path

class CommonGatewayInterface:

    def __init__(self, resourcePath, conn, headerFields, operation):
        self.headerFields = headerFields
        self.conn = conn
        self.operation = operation
        self.resourcePath = resourcePath
        self.file = open(self.resourcePath, "r")

        self.readFile()         # get only the CGI
        self.joinCGI()
        self.file.close()
        self.sendAndSolveInstructions()
        print(self.dyn)

    def readFile(self):
        lines = self.file.readlines()
        self.dyn = ""

        lastI = 0
        for i in range(0, len(lines)):
            lastI = i
            if(lines[i].find("<%") != -1):
                if (lines[i].find("%>") != -1):
                    self.dyn = lines[i][lines[i].find("<%"):lines[i].find("%>")]
                    return
                else:
                    self.dyn = lines[i][lines[i].find("<%"):]
                    break

        lastI += 1
        for i in range(lastI, len(lines)):
            if (lines[i].find("%>") != -1):
                self.dyn += lines[i]
                break
            else:
                self.dyn += lines[i][:lines[i].find("%>")]

    def joinCGI(self):
        # remove all break line
        self.dyn = self.dyn.replace("\r", "")
        self.dyn = self.dyn.replace("\n", "")
        # remove all space in the string
        self.dyn = self.dyn.replace(" ", "")

        self.dyn = self.dyn[2:-3]           # remove the '<%' and ';%>'
        self.dyn = self.dyn.split(";")      # separe the instructions

    def sendAndSolveInstructions(self):

        self.file = open(self.resourcePath, "r")
        lines = self.file.readlines()

        response = 'HTTP/1.1 200 OK\r\n' + \
                   'Server: Venturini/1.1\r\n' + \
                   'Date: ' + self.operation.getCurrentDate() + '\r\n' + \
                   'Last-Modified: ' + self.operation.lastModified(self.resourcePath, False) + '\r\n' + \
                   'Set-Cookie: ' + self.operation.getCookies() + '\r\n\r\n'

        self.conn.sendall(response.encode())

        input = False
        for i in range(0, len(lines)):
            if (lines[i].find("<%") != -1):
                input = True
                continue

            if(input):
                if (lines[i].find("%>") == -1):
                    self.conn.sendall(self.getSolved(lines[i].replace(" ", "")).encode())
                    continue
                else:
                    input = False
                    continue

            self.conn.sendall(lines[i].encode())

    def getSolved(self, method):
        if(method.__contains__("%>")):
            return ""

        if("getHeaderField" == method[:method.index("(")]):
            return method[method.index("\""):-3]
        elif("date" == method[:method.index("(")]):
            return self.operation.getCurrentDate()