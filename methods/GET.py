# -*- coding:ISO-8859-1 -*-
import base64                   # base64.b64decode()
import _md5                     # _md5.new(pass).hexdigest()
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

        # if is folder, need to allow from basic authentication
        if(path.exists(self.resourcePath + '/') and self.canAccess() == False):
            self.response.response401(self.realm)
            return

        if(self.conditionals() == True):
            return

        # else, get the file or index.html if the resourcePath is a path
        self.response.response200(self.headerFields)

    def canAccess(self):
        # if the resource is a path, check the exist of a .htaccess
        self.realm = "Please, send the user and pass."
        try:
            htaccess = open(self.resourcePath + '/.htaccess').readlines()
        except IOError:         # if get the except, then file .htaccess not exists. Then return the path
            return True

        # .htaccess existing. then check the credentials
        # if the request send the credentials, get it. If no, get the except
        try:
            credentials = self.headerFields["Authorization"].split(' ')[1]
        except (KeyError, IndexError):
            print("The request not send a credentials")
            return False

        # then get the files where existing the pass
        htpasswd = ""
        for i in range(0, len(htaccess)):               # iteration at the find the field .htpasswd
            if(htaccess[i].find("AuthName") != -1):     # search the AuthName
                self.realm = htaccess[i].split(" \"")[1][:-1]       # get the realm to send a response 401
                self.realm = self.realm.rstrip()                    # remove the '\n'

            if(htaccess[i].find("AuthUserFile") != -1):     # search the file of a .htpasswd
                htpasswd = htaccess[i].split(" ")[1][:-1]   # get the second field, the locate of file .htpasswd
                htpasswd = htpasswd.rstrip()            # remove the '\n'

        # the credentials is get and file htpasswd
        try:
            htpasswd = open(htpasswd).readlines()
            # iterate in the .htpasswd to find the credentials
            credentials = base64.b64decode(credentials).split(':')
            for i in range(0, len(htpasswd)):
                line = htpasswd[i].rstrip()     # get the credentials in the .htaccess
                credTemp = line.split(':')      # split the line in user:pass
                if(credTemp[0] == credentials[0] and credTemp[1] == _md5.new(credentials[1]).hexdigest()):
                    return True     # user and pass is found

            print("User or pass is incorrect")
            return False
        except (TypeError, IOError):
            print("Probaly, the file " + htpasswd + " is not exists")
            return False

    def conditionals(self):     # If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match or If-Range

        keys = list(self.headerFields.keys())
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
        try:                                                                        # some browers send the ifModifiedSince brokes. Example, the Opera send 'Wed, 11 Apr 2018 1'
            t = self.headerFields["If-Modified-Since"]
            dateClient = datetime.strptime(t, "%a, %d %b %Y %H:%M:%S %Z")           # Wed, 21 Oct 2015 07:28:00 GMT
            dateServer = self.operation.lastModified(self.resourcePath, True)       # True = get the Object date
        except ValueError:
            print("Cannot possible verify the If-Modified-Since: " + self.headerFields["If-Modified-Since"])
            return False

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