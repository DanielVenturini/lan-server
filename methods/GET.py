# -*- coding:ISO-8859-1 -*-

from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getsize()
import time                     # time.localtime()
import mimetypes                # mimetypes.guess_type()

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
        if(path.isfile(self.resourcePath) == False):    # file not exists
            self.conn.sendall('HTTP/1.1 404 Not Found\r\n\r\n')
            return

        if(self.conditionals() == False):           # the Cliente be the file actual
            self.conn.sendall('HTTP/1.1 304 Not Modified\r\n\r\n')
            return

        # else, get the file
        try:

            response = 'HTTP/1.1 200 OK\r\n' +\
                       'Server: Venturini/1.1\r\n' +\
                       'Content-Length: ' + str(path.getsize(self.resourcePath)) + '\r\n' +\
                       'Content-Type: ' + mimetypes.guess_type(self.resourcePath)[0] + '\r\n' +\
                       'Last-Modified: ' + self.lastModified(False) + "\r\n\r\n"                    # get the string date

            self.conn.sendall(response)
            print("RETURN THE FILE " + self.resourcePath + "\n")

            file = open(self.resourcePath, "r")
            bytesSequence = file.read(self.size)        # read only 128 bytes in each loop
            while(bytesSequence!= ""):
                self.conn.sendall(bytesSequence)        # send the 128 bytes
                bytesSequence = file.read(self.size)    # get nexts 128 bytes

        except (IOError, OSError):
            print("FILE NOT FOUND" + self.resourcePath)
            self.conn.sendall("HTTP/1.1 404 Not Found\r\n\r\n")

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

    # if the file in Cliente be actual, dont return
    def returnFile(self, dateClient, dateServer):
        if(dateClient >= dateServer):
            print("The file on the Client is current\n")
            return False
        else:
            print("The file on the client is not current\n")
            return True

    # implementation of If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

    def ifModifiedSince(self):
        t = self.hash["If-Modified-Since"]
        dateClient = datetime.strptime(t, "%a, %d %b %Y %H:%M:%S %Z")   # Wed, 21 Oct 2015 07:28:00 GMT
        dateServer = self.lastModified(True)                            # get the Object date

        return self.returnFile(dateClient, dateServer)

    def ifNoneMatch():
        pass

    def lastModified(self, getDate):    # get the Object date or string with the date of last modified
        date = ['Mon, ', 'Tue, ', 'Wed, ', 'Thu, ', 'Fri, ', 'Sat, ', 'Sun, ']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        t = time.localtime(path.getmtime(self.resourcePath))            # get the time of file on server
        strDate = date[t.tm_wday]
        date = datetime.strptime(strDate + str(t.tm_mday) + " " + str(t.tm_mon) + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT", "%a, %d %m %Y %H:%M:%S %Z")
        strDate += str(t.tm_mday) + " " + month[t.tm_mon-1] + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT"

        if(getDate):
            return date
        else:
            return strDate