# -*- coding:ISO-8859-1 -*0

from interface import interface

class Virtual:

    def __init__(self, get):
        self.get = get

    def start(self):            # is not a thread
        if(self.getResource() == False):
            self.get.response.response404()
            return

        self.getVirtual()

    def getResource(self):
        try:
            self.resourcePath = self.get.resourcePath

            self.resourcePath = self.resourcePath[self.resourcePath.rindex('/')+1:]     # http://host:80/virtual/telemetria/status.json -> 'status.json'
            self.virtual = self.resourcePath[:self.resourcePath.rindex('.')]            # status.json -> 'status'
            return True

        except ValueError:      # the user can send the requeste 'status' without '.json'
            return False

    def getVirtual(self):
        if(self.virtual == "status"):
            self.getStatus()
        else:
            self.get.response.response404()

    def getStatus(self):
        responseClient = 'HTTP/1.1 404 Not Found\r\n ' + \
       'Server: Venturini/1.1\r\n' + \
       'Date: ' + self.get.operation.getCurrentDate() + '\r\n' + \
       'Set-Cookie: ' + self.get.operation.getCookies() + '\r\n' + \
       'Content-Type: text/html\r\n\r\n' + \
        interface.getHeader('Status', 'Telemetria Status', self.get.parent) +\
       '<p> number of requests met: ' + str(self.get.reqCount) + ' </p>\r\n' + \
       '<p> server up time: ' + self.get.upTime + ' </p>\r\n' +\
       '<p> conected servers: ' + self.conectedServers() +\
        interface.getTail()

        self.get.response.send(responseClient)

    def conectedServers(self):
        resp = ''
        for address in self.get.servers.keys():
            port = self.get.servers[address]
            resp += ('<p>' + address + ':' + port + '</p>')

        if(resp == ''):
            return '<p> 0 servers </p>'
        else:
            return resp