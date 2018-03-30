# -*- coding:ISO-8859-1 -*-
from os import path             # os.path.getsize()
from datetime import datetime   # datetime.strptime()
from methods import Response
from methods import Operation

class GET():

    def __init__(self, resourcePath, hash, conn, cookies):
        self.headerFields = hash
        self.operation = Operation.Operation(cookies)

        self.resourcePath = self.operation.getResourcePathName(resourcePath)

        self.response = Response.Response(conn, self.resourcePath, cookies)

    def getResponse(self):
        if(path.isfile(self.resourcePath) == False):    # file not exists
            self.response.response404()
            return

        if(self.conditionals() == True):
            return

        # else, get the file
        self.response.response200()

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