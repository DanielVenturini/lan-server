# -*- coding:ISO-8859-1 -*-
from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getsize()
import time                     # time.localtime()

class GET():

    def __init__(self, resourcePath, hash):
        self.hash = hash
        self.resourcePath = resourcePath
        # If '/', return index.html. Some browers request from the 'favicon.ico' of the page. If none, concat the '.'
        if(self.resourcePath == "/"): self.resourcePath = "./index.html"
        elif(self.resourcePath == "/favicon.ico"): self.resourcePath = "./photos/favicon.ico"
        else: self.resourcePath = "." + resourcePath

    def getFile(self):
        if(self.conditionals() == False):
            return 'HTTP/1.1 304 Not Modified\r\n'

        try:
            print("RETURN THE FILE " + self.resourcePath)
            return 'HTTP/1.1 200 OK\r\nServer: Venturini/1.1\r\n\r\n' + open(self.resourcePath, "r").read()
        except IOError:
            print("FILE NOT FOUND" + self.resourcePath)
            return "HTTP/1.1 404 Not Found\r\n"

    def conditionals(self): #If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

        keys = self.hash.keys()
        if(keys.count("If-Modified-Since") != 0): #If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
            dateClient = datetime.strptime(self.hash["If-Modified-Since"], "%a, %d %b %Y %I:%M:%S %Z")
            dateServer = time.localtime(path.getmtime(self.resourcePath))

            return self.returnFile(dateClient, dateServer)

        elif(keys.count("If-Unmodified-Since") != 0):
            pass
        elif(keys.count("If-Match") != 0):
            pass
        elif(keys.count("If-None-Match") != 0):
            pass
        elif(keys.count("If-Range") != 0):
            pass

    def returnFile(self, dateClient, dateServer):
        if(int(dateClient.year) < (dateServer.tm_year)):
            return True
        if(int(dateClient.month) < int(dateServer.tm_mon) and int(dateClient.year) <= (dateServer.tm_year)):
            return True
        if(int(dateClient.day) < int(dateServer.tm_mday) and int(dateClient.month) <= int(dateServer.tm_mon)):
            return True
        if(int(dateClient.hour) < int(dateServer.tm_hour) and int(dateClient.day) <= int(dateServer.tm_mday)):
            return True
        if(int(dateClient.minute) < int(dateServer.tm_min) and int(dateClient.hour) <= int(dateServer.tm_hour)):
            return True

        return False