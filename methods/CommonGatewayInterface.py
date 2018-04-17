# -*- coding: ISO-8859-1 -*-
import shutil                   # shutil.which("/bin/ps")
from methods import Response

class CommonGatewayInterface:

    def __init__(self, resourcePath, conn, headerFields, operation, query, parent):
        self.headerFields = headerFields
        self.conn = conn
        self.operation = operation
        self.resourcePath = resourcePath
        self.query = query
        self.parent = parent

        self.executeWhat()

    # if the resourcePath is CGI, execute in the SO and return the result; else, the resource is a file.dyn
    def executeWhat(self):
        print("Atual pai de todos aqui: " + self.parent)
        if(self.parent == '/CGI'):
            self.executeSOAndReturn()
        else:
            self.file = open(self.resourcePath, "r")
            self.sendAndSolveInstructions()

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
            if (lines[i].find("<%") != -1):         # if this line contains '<%', set the input with true to get the instructs
                input = True
                continue

            if(input):                              # getting the instructs
                if (lines[i].find("%>") == -1):     # if this line not contains '%>'
                    self.conn.sendall(self.getSolved(lines[i].replace(" ", "")).encode())   # send the instruct resolved
                    continue
                else:
                    input = False
                    continue

            self.conn.sendall(lines[i].encode())    # send the normal lines

    def getSolved(self, method):
        if("getHeaderField" == method[:method.index("(")]):

            try:
                return self.headerFields[method[method.index("\"")+1:-4]] + '\n'
            except KeyError:
                return 'None\n'

        elif("date" == method[:method.index("(")]):
            return self.operation.getCurrentDate() + '\n'

    def executeSOAndReturn(self):
        if(shutil.which("/bin/" + self.resourcePath[6:]) == None):
            Response.Response(self.conn, self.resourcePath, self.cookies, self.query, self.parent).response404()
        else:
            print("Arquivo quernedo ser executado")