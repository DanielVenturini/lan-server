# -*- coding:ISO-8859-1 -*-
from interface import interface # interface.getHeader()
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

    def getStringLastModified(self, date):
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        dateStr = str(date.day) + ' ' + month[date.month-1] + ' ' + str(date.year) + ' ' + str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)
        return dateStr

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

        indexhtml = interface.getHeader('Index of '+resourcePath, 'List of files in ' + resourcePath[1:], self.parent)
        indexhtml += '<table><tr><td><img src="data:image/png;base64, R0lGODlhFAAWAKEAAP///8z//wAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAACE4yPqcvtD6OctNqLs968+w+GSQEAOw=="></td><td><h2><a href="'+self.queryN+'">File</a></h2></td><td><h2><a href="'+self.queryS+'">Size</a></h2></td><td><h2>Last Modified</h2></td></tr><hr>\r\n'

        for i in range(0, len(self.files)):
            nameFile = self.files[i]
            if(self.files[i] == '.htpasswd'):       # not list the file .htpasswd, if is in this path
                continue

            if(resourcePath == './'):
                self.files[i] = resourcePath + self.files[i]
            else:
                self.files[i] = resourcePath + '/' + self.files[i]

            if(path.isfile(self.files[i])):
                icon = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAZCAYAAAAxFw7TAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4gMfECgkpfrEOwAAAZBJREFUOMvllL2KIkEUhU9ZLYo/SGlLBYKUCOPQysaTmIwbGgkGRr6FD+ELLIiPYbahGxiYTODMYLAomCgoDNIauN1ngmGEXnbZ1elgYU9SVPLdr+69lKhWqw+73e6T53nwfR++7wPA+fxd0un0c6FQuJtMJi8A0Ov10O/3IbTW3Gw2MMaAJP4UIQRWqxVOpxOUUo+1Wu1+PB6vAWAwGAC2bbNcLvOSOI7DUqlEAFRKTRuNhjlXzGazFwONMRwOh2y32wRA27a/NZvNGwCAUupiYLFY5Gg04n6/Z7fbJQDm8/mv9Xq9aP1N335OJBLBfD6HMQadTgez2QzT6fSzEOILMpnMxYaVSoXJZJK5XI5KKUopCYBSyh9XAY/HI13Xpeu6PBwOXC6XbLVaBEALVyQejwfuiUQClvWGilzTw1/tphAiPGBgYGGBzoYIOf+R4b8NDOxh6Ibv5NCmHBYwVMNAD6WU+Cg0lUohGo0CAKxYLIbFYgHHcXDtR+F5Htbr9Zut1vppu93efvTZJKG1/v4KXBt17n/ZwIoAAAAASUVORK5CYII='
            else:
                icon = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAASCAYAAABb0P4QAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAk6NAAJOjQFAepa8AAAAB3RJTUUH4gMfDxkNNm+/qAAAAOZJREFUOMvtjz0vBGEYRc/zzjuxOqEwEd0qiFKh0GnE75CtN9pt7LZU/sqq5heIqDahUFFpjMQkOzGf76MRiRhjwxSKPfXNuffK1jD0gQFwDHh8RoA74MgIk9uTA+UHZHMYrjglKl1jNs8rzrJSb4CvQcGpch2dHj7IzuhieX2p87y35uOZepvqx9zaVqfI5Km8uo+m+3Yx2OhWfsXlq/f+sPnRN5WUHbcrq2bbpmrHj7mFjL8hYGBsgcAwy7iZCAwtMxfOhf9EqC3qFFMkcdqWrkji1BbTl16RxOcgC/x+roBmqPbfAHgKT43q9FtmAAAAAElFTkSuQmCC'

            indexhtml += ('<tr><td><img src="data:image/png;base64,'+icon+'"></td><td><a href='+self.files[i][1:]+'>'+nameFile+'</a></td><td>'+self.getSize(self.hashSize[nameFile])+'</td><td>'+self.hashLast[nameFile]+'<td></tr>\r\n') # new register in the table

        indexhtml += '</table>\r\n' + interface.getTail()

        return indexhtml

    def orderByQuery(self, resourcePath):

        self.queryN = '?R=N;O=C'
        self.queryS = '?R=S;O=C'

        self.hashSize = {}
        self.hashLast = {}

        if(self.query[2] == 'N'):           # Reference by Name of file
            self.sortByName(resourcePath)

        if(self.query[2] == 'S'):           # Reference by Size of file
            self.sortBySize(resourcePath)

    def sortByName(self, resourcePath):

        self.files = sorted(self.files, key=str.lower)  # Default order by Crescent
        self.queryN = "?R=N;O=D"
        if(self.query[6] == 'D'):                       # Order by Decreasing
            self.files.reverse()
            self.queryN = "?R=N;O=C"

        for i in range(0, len(self.files)):

            if(resourcePath != './'):
                resourcePath += '/'

            if (path.isfile(resourcePath + self.files[i])):
                self.hashSize[self.files[i]] = path.getsize(resourcePath + self.files[i])
            else:
                self.hashSize[self.files[i]] = -1

            self.hashLast[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]

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
                self.hashLast[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]
                continue

            self.hashSize[path.getsize(resourcePath + self.files[i])] = self.files[i]
            self.hashLast[self.files[i]] = self.lastModified(resourcePath + self.files[i], False)[5:-4]

        size = list(self.hashSize.keys())      # get all the keys size
        size.sort()                         # sort this keys
        self.queryS = '?R=S;O=D'            # new query if Order be Crescent

        if(self.query[6] == 'D'):
            size.reverse()              # sort by Decreasing
            self.queryS = '?R=S;O=C'

        last = 0

        # put the paths in the hash
        if(self.hashSize[-1] != []):
            for i in range(0, len(self.hashSize[-1])):
                self.files[i] = self.hashSize.get(-1)[i]
                self.hashSize[self.files[i]] = -1
                last = i + 1

        # put the files in the hash
        for i in range(0, len(size)):
            if(size[i] == -1):
                continue

            self.files[last] = self.hashSize[size[i]]
            self.hashSize[self.files[last]] = size[i]
            last += 1
