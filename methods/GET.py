# -*- coding:ISO-8859-1 -*-
from os import path             # os.path.getsize()
from datetime import datetime   # datetime.strptime()
from methods import Response
from methods import Operation

class GET():

    def __init__(self, resourcePath, hash, conn, cookies, query, parent):
        self.headerFields = hash
        self.parent = parent
        self.operation = Operation.Operation(cookies, query, parent)

        self.resourcePath = self.operation.getResourcePathName(resourcePath)

        self.response = Response.Response(conn, self.resourcePath, cookies, query, parent)

    def getResponse(self):
        # if resourcePath is not a file or path, sending 404
        if(path.exists(self.resourcePath) == False):        # is not a file too is not a path
            self.response.response404()
            return

        if(path.exists(self.resourcePath + '/') and self.canAccess() == False):
            self.response.response401()

        if(self.conditionals() == True):
            return

        # else, get the file or index.html if the resourcePath is a path
        self.response.response200()

    def canAccess(self):
        try:
            credentials = self.headerFields["Authorization"]
        except KeyError:
            print("Nao foi enviado credenciais")
            return False
        else:
            print("Foi enviado as credenciais")
            return True

    def conditionals(self):     # If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

        keys = self.headerFields.keys()
        if(keys.count("If-Modified-Since") != 0):                   # If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
            return self.ifModifiedSince()

        elif(keys.count("If-Unmodified-Since") != 0):
            return self.ifUnmodifiedSince()

        elif(keys.count("If-Match") != 0):
            pass
        elif(keys.count("If-None-Match") != 0):
            return self.ifNoneMatch()
        elif(keys.count("If-Range") != 0):
            pass

    # implementation of If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range
    def ifModifiedSince(self):
        t = self.headerFields["If-Modified-Since"]
        dateClient = datetime.strptime(t, "%a, %d %b %Y %H:%M:%S %Z")       # Wed, 21 Oct 2015 07:28:00 GMT
        dateServer = self.operation.lastModified(self.resourcePath, True)        # True = get the Object date

        if(self.operation.currentFile(dateClient, dateServer) == "CLIENT"):
            print("The file on the Client is current\n")
            self.response.response304()                                     # return only this header
            return True
        else:
            print("The file on the client is not current\n")
            return False                                                    # need send the current file in Server

    def ifUnmodifiedSince(self):
        t = self.headerFields["If-Unmodified-Since"]
        dateClient = datetime.strptime(t, "%a, %d %b %Y %H:%M:%S %Z")       # Wed, 21 Oct 2015 07:28:00 GMT
        dateServer = self.operation.lastModified(self.resourcePath, True)        # get the Object date

        if(self.operation.currentFile(dateClient, dateServer) == "CLIENT"):
            print("The file on the Server has not been modified")
            return False                                                    # execute the method
        else:
            print("The file on the Server has been modified")
            self.response.response412()                                     # return only this header
            return True