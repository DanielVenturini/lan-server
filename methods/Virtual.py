# -*- coding:ISO-8859-1 -*0

from interface import interface
from methods.Operation import Operation

class Virtual:

    def __init__(self, get):
        self.method = get

    def start(self):            # is not a thread
        if(self.getResource() == False):
            self.method.response.response404()
            return

        self.getVirtual()

    def getResource(self):
        try:
            self.resourcePath = self.method.resourcePath

            if(self.resourcePath.__contains__('requests')):
                self.virtual = 'requests'
                return True

            if(self.resourcePath.__contains__('connecteds')):
                self.virtual = 'connecteds'
                return True

            # http://host:80/virtual/telemetria/status.json -> 'virtual/telemetria/status.json'
            if(self.resourcePath[self.resourcePath.rindex('.')+1:].__eq__('json')):
                self.virtual = self.resourcePath[1:self.resourcePath.rindex('.')]            # status.json -> 'status'
                return True
            else:
                return False

        except ValueError:      # the user can send the requeste 'status' without '.json'

            if(self.resourcePath.__contains__('feedback')):   # if it's feedback, it dosen't have the point
                self.virtual = 'feedback'
                return True

            return False        # it's not status ou feedback

    def getVirtual(self):
        try:
            if(self.virtual.__eq__('/virtual/telemetria/status')):
                self.getStatus()
            elif(self.virtual.__eq__('feedback')):
                self.saveFeedback()
            elif(self.virtual.__eq__('requests')):
                self.sendRequestsToAngular()
            elif(self.virtual.__eq__('connecteds')):
                self.sendConnectedsToAngular()
            else:
                self.method.response.response404()
        except AttributeError:
            self.method.response.response404()

    def sendRequestsToAngular(self):
        self.method.response.send(str(self.method.reqCount))

    def sendConnectedsToAngular(self):
        self.method.response.send(self.conectedServers())

    def getStatus(self):
        responseClient = 'HTTP/1.1 200 OK\r\n ' + \
        'Server: Venturini/1.1\r\n' + \
        'Date: ' + self.method.operation.getCurrentDate() + '\r\n' + \
        'Set-Cookie: ' + self.method.operation.getCookies() + '\r\n' + \
        'Content-Type: text/html\r\n\r\n' + \
                interface.getHeader('Status', 'Telemetria Status', self.method.parent) +\
        '<div ng-app="Venturini/1.1" ng-controller="myCtrl">\r\n' \
        '   <p> number of requests met: {{requests}} </p>\r\n' + \
        '   <p> server up time: ' + self.method.upTime + ' </p>\r\n' +\
        '   <p> conected servers: {{connecteds}} </p>\r\n' \
        '</div>\r\n' +\
        '\r\n' +\
        '<script>\r\n' +\
        '   var app = angular.module(\'Venturini/1.1\', []);\r\n' +\
        '   app.controller(\'myCtrl\', function($scope, $http) {\r\n' + \
        '       $http.get("requests") \r\n' +\
        '       .then(function(response){ \r\n' +\
        '           $scope.requests = response.data; \r\n' +\
        '       });\r\n' +\
        '       $http.get("connecteds") \r\n' +\
        '       .then(function(response){ \r\n' +\
        '           $scope.connecteds = response.data; \r\n' +\
        '       });\r\n' +\
        '   });\r\n' +\
        '</script>\r\n' +\
        interface.getTail()

        self.method.response.send(responseClient)

    def conectedServers(self):
        resp = ''
        for address in self.method.servers.keys():
            port = self.method.servers[address]
            resp += (address + ':' + port + '<br>')

        if(resp == ''):
            return '0 servers'
        else:
            return resp

    def saveFeedback(self):
        bodyLines = self.method.httpBody[-1].split('&') # separe in lines
        self.saveFromBody(bodyLines)                    # separe all header and values

    def saveFromBody(self, bodyLines):

        nameFile = Operation(None, None, None).getCurrentDate()         # only get the current date to be the of file
        file = open('feedback/' + self.parseDate(nameFile), 'w+')       # create a new file

        for line in bodyLines:
            line = line.split('=')
            file.write(line[0] + ' \'' + line[1].replace('%2C', ', ').replace('+', ' ') + '\'\r\n')

        try:
            file.write('Host ' + self.method.headerFields['Host'] + '\r\n')
            file.write('Referer ' + self.method.headerFields['Referer'] + '\r\n')
            file.write('Cookie ' + self.method.cookies + '\r\n')
            file.write('User-Agent ' + self.method.headerFields['User-Agent'] + '\r\n')
        except KeyError:
            pass
        except :
            pass

        file.close()

    # transform 'Mon, 21 May 2018 23:35:17 GMT' in 'Mon21May201823:35:17GMT'
    def parseDate(self, date):
        return date.replace(' ', '').replace(',', '')