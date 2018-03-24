# -*- coding:ISO-8859-1 -*-
from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getsize()
import time                     # time.localtime()

class GET():

    def __init__(self, resourcePath, hash, conn):
        self.conn = conn
        self.hash = hash
        self.resourcePath = resourcePath
        self.size = 128     # size of bytes to read and send
        # If '/', return index.html. Some browers request from the 'favicon.ico' of the page. If none, concat the '.'
        if(self.resourcePath == "/"): self.resourcePath = "./index.html"
        elif(self.resourcePath == "/favicon.ico"): self.resourcePath = "./photos/favicon.ico"
        else: self.resourcePath = "." + resourcePath

    def getFile(self):
        if(self.conditionals() == False):           # the Cliente be the file actual
            return 'HTTP/1.1 304 Not Modified\r\n\r\n'

        # else, get the file
        try:

            print("RETURN THE FILE " + self.resourcePath)
            response = 'HTTP/1.1 200 OK\r\n' +\
                       'Server: Venturini/1.1\r\n' +\
                       'Content-Length: ' + str(path.getsize(self.resourcePath)) + '\r\n\r\n'

            self.conn.sendall(response)

            file = open(self.resourcePath, "r")
            bytesSequence = file.read(self.size)        # read only 128 bytes in each loop
            while(bytesSequence!= ""):
                self.conn.sendall(bytesSequence)        # send the 128 bytes
                bytesSequence = file.read(self.size)    # get nexts 128 bytes

        except (IOError, OSError):
            print("FILE NOT FOUND" + self.resourcePath)
            return "HTTP/1.1 404 Not Found\r\n"

    def conditionals(self):     # If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

        keys = self.hash.keys()
        if(keys.count("If-Modified-Since") != 0):   # If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
            return self.ifModifiedSince()

        elif(keys.count("If-Unmodified-Since") != 0):
            pass
        elif(keys.count("If-Match") != 0):
            pass
        elif(keys.count("If-None-Match") != 0):
            return self.ifNoneMatch()
        elif(keys.count("If-Range") != 0):
            pass

    def returnFile(self, dateClient, dateServer):
        if(dateClient > dateServer):
            return False

    # implementation of If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

    def ifModifiedSince():
        t = self.hash["If-Modified-Since"]
        dateClient = datetime.strptime(t[5:-4], "%d %b %Y %H:%M:%S")    # Wed, 21 Oct 2015 07:28:00 GMT => 21 Oct 2015 07:28:00
        t = time.localtime(path.getmtime(self.resourcePath))            # get the time of file on server
        dateServer = datetime.strptime(str(t.tm_mday) + " " + str(t.tm_mon) + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec), "%d %m %Y %H:%M:%S")

        return self.returnFile(dateClient, dateServer)

    def ifNoneMatch():
        pass