# -*- coding:ISO-8859-1 -*-
from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getmtime()
import time                     # time.localtime()
import os                       # os.listdir()

class Operation:

    def __init__(self, cookies, query, parent):
        self.query = query
        self.cookies = cookies
        self.parent = parent

    def currentFile(self, dateClient, dateServer):
        if(dateClient >= dateServer):
            return "CLIENT"
        else:
            return "SERVER"

    def lastModified(self, resourcePath, getDate):      # get the Object date or string with the date of last modified
        date = ['Mon, ', 'Tue, ', 'Wed, ', 'Thu, ', 'Fri, ', 'Sat, ', 'Sun, ']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        t = time.localtime(path.getmtime(resourcePath))             # get the time of file on server
        strDate = date[t.tm_wday]
        date = datetime.strptime(strDate + str(t.tm_mday) + " " + str(t.tm_mon) + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT", "%a, %d %m %Y %H:%M:%S %Z")
        strDate += str(t.tm_mday) + " " + month[t.tm_mon-1] + " " + str(t.tm_year) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + " " + " GMT"

        if(getDate):
            return date
        else:
            return strDate

    def getCookies(self):
        if(self.cookies == {}):
            return "count=0"
        else:
            return "count=" + str(int(self.cookies["count"])+1)

    def getResourcePathName(self, resourcePath):
        # If '/', return index.html. Some browers request from the 'favicon.ico' of the page. If none, concat the '.'
        if(resourcePath == "/index.html"): resourcePath = "/"
        elif(resourcePath == "/favicon.ico"): resourcePath = "/photos/favicon.ico"
        else: resourcePath = "." + resourcePath

        return resourcePath

    def getCurrentDate(self):
        weekday = ['Mon, ', 'Tue, ', 'Wed, ', 'Thu, ', 'Fri, ', 'Sat, ', 'Sun, ']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        propertyTime = time.localtime()
        strDate = ""            # Wed, 21 Oct 2015 07:28:00 GMT

        strDate += weekday[propertyTime.tm_wday]
        strDate += (str(propertyTime.tm_mday) + ' ')
        strDate += (month[propertyTime.tm_mon-1] + ' ')
        strDate += (str(propertyTime.tm_year) + ' ')
        strDate += (str(propertyTime.tm_hour) + ':')
        strDate += (str(propertyTime.tm_min) + ':')
        strDate += (str(propertyTime.tm_sec) + ' GMT')

        return strDate

    def getSize(self, size):
        if(size == -1):
            return '---'

        sizeFull = ""
        if(size < 1000):
            return str(size) + ' bytes'
        elif(size < 1e+6):
            return str(int(size/1000)) + ',' + str(int((size%1000)/100)) + ' kB'
        elif(size < 1e+9):
            return str(int(size/1e+6)) + ',' + str(int((size%1e+6)/1e+5)) + ' MB'
        else:
            return str(int(size/1e+9)) + ',' + str(int((size%1e+9)/1e+8)) + ' GB'

    def getIndex(self, resourcePath):

        self.files = os.listdir(resourcePath)
        self.orderByQuery(resourcePath)
        print("Tudo em files: ", self.files)

        indexhtml = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\r\n' +\
                    '<html>\r\n' +\
                    '<head>\r\n' +\
                        '<meta charset="utf-8"/>\r\n' +\
                        '<title>Index of ' + resourcePath + '</title>\r\n' +\
                    '</head>\r\n' +\
                    '<body style="background-color:AliceBlue">\r\n' +\
                        '<div style="background-color:yellow">\r\n' +\
                            '<hr><h1>List of files in ' + resourcePath[1:] + '</h1><hr>\r\n' +\
                        '</div>\r\n' +\
                    '<table cellspacing="10"><tr><td><img src="/photos/index.png"></td><td><h2><a href="'+self.queryN+'">File</a></h2></td><td><h2><a href="'+self.queryS+'">Size</a></h2></td><td><h2><a href="'+self.queryL+'">Last Modified</a></h2></td></tr><hr>\r\n' +\
                    '<tr><td><img src="/photos/parent-icon.png"></td><td><a href='+self.parent+'>Parent Directory</a></td><td></td><td><td></tr>\r\n'

        for i in range(0, len(self.files)):
            nameFile = self.files[i]

            if(resourcePath == './'):
                self.files[i] = resourcePath + self.files[i]
            else:
                self.files[i] = resourcePath + '/' + self.files[i]

            if(path.isfile(self.files[i])):
                icon = '/photos/file-icon.png'
            else:
                icon = '/photos/folder-icon.png'

            indexhtml += ('<tr><td><img src='+icon+'></td><td><a href='+self.files[i][1:]+'>'+nameFile+'</a></td><td>'+self.getSize(self.hashSize[nameFile])+'</td><td>'+self.hashTime[nameFile]+'<td></tr>\r\n') # new register in the table

        indexhtml += '</table><hr><address>Venturini/1.1 -- '+self.getCurrentDate()+'</address></body></html>'

        return indexhtml

    def orderByQuery(self, resourcePath):

        self.queryN = '?R=N;O=C'
        self.queryS = '?R=S;O=C'
        self.queryL = '?R=L;O=C'

        self.hashSize = {}
        self.hashTime = {}

        if(self.query[2] == 'N'):       # Reference by Name of file
            self.sortByName(resourcePath)

        if(self.query[2] == 'S'):           # Reference by Size of file
            self.sortBySize(resourcePath)

        if(self.query[2] == 'L'):       # Reference by LastModified of file
            self.files.sort()                # Default order by Crescent
            if(self.query[6] == 'D'):   # Order by Decreasing
                pass

    def sortByName(self, resourcePath):
        self.files.sort()           # Default order by Crescent
        self.queryN = "?R=N;O=D"
        if(self.query[6] == 'D'):   # Order by Decreasing
            self.files.reverse()
            self.queryN = "?R=N;O=C"

        for i in range(0, len(self.files)):

            if(resourcePath != './'):
                resourcePath += '/'

            if (path.isfile(resourcePath + self.files[i])):
                self.hashSize[self.files[i]] = path.getsize(resourcePath + self.files[i])
            else:
                self.hashSize[self.files[i]] = -1

            self.hashTime[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]

    def sortBySize(self, resourcePath):

        size = []
        self.hashSize[-1] = []

        if (resourcePath != './'):
            resourcePath += '/'

        for i in range(0, len(self.files)):

            if(path.isfile(resourcePath + self.files[i]) == False):
                size = self.hashSize[-1]
                size.append(self.files[i])
                self.hashSize[-1] = size
                self.hashTime[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]
                continue

            self.hashSize[path.getsize(resourcePath + self.files[i])] = self.files[i]
            self.hashTime[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]

        size = self.hashSize.keys()      # get all the keys size
        size.sort()                         # sort this keys
        self.queryS = '?R=S;O=D'            # new query if Order be Crescent

        if(self.query[6] == 'D'):
            size.reverse()              # sort by Decreasing
            self.queryS = '?R=S;O=C'

        print("Todas as pastas: ", self.hashSize[-1])
        print("Todos os arquivos: ", self.hashSize.keys())
        last = -1

        # put the paths in the hash
        if(self.hashSize[-1] != []):
            for i in range(0, len(self.hashSize[-1])):
                self.files[i] = self.hashSize.get(-1)[i]
                self.hashSize[self.files[i]] = -1
                last = i

        # put the files in the hash
        for i in range(0, len(size)-1):
            if(size[i] == -1):
                continue

            self.files[last+i+1] = self.hashSize[size[i]]
            self.hashSize[self.files[last+i+1]] = size[i]
        print("Todas as chavem em size: ", self.hashSize)