# -*- coding:ISO-8859-1 -*-
from datetime import datetime   # datetime.strptime()
from os import path             # os.path.getmtime()
import time                     # time.localtime()
import os                       # os.listdir()

class Operation:

    def __init__(self, cookies):
        self.cookies = cookies

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
                    '<table cellspacing="10"><tr><td><img src="/photos/index.png"></td><td><h2>File</h2></td><td><h2>Size</h2></td><td><h2>Last Modified</h2></td></tr><hr>\r\n'

        files = os.listdir(resourcePath)
        for i in range(0, len(files)):
            nameFile = files[i]
            size = ''

            if(resourcePath == './'):
                files[i] = resourcePath + files[i]
            else:
                files[i] = resourcePath + '/' + files[i]

            if(path.isfile(files[i])):
                icon = '/photos/file-icon.png'
                size = self.getSize(path.getsize(files[i]))
            else:
                icon = '/photos/folder-icon.png'
                size = '—'

            indexhtml += ('<tr><td><img src='+icon+'></td><td><a href='+files[i][1:]+'>'+nameFile+'</a></td><td>'+size+'</td><td>'+self.lastModified(files[i], False)[5:-4]+'<td></tr>\r\n') # new register in the table

        indexhtml += '</table><hr><address>Venturini/1.1 -- '+self.getCurrentDate()+'</address></body></html>'

        return indexhtml