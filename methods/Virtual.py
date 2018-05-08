# -*- coding:ISO-8859-1 -*0

class Virtual:

    def __init__(self, response):
        self.response = response

    def start(self):            # is not a thread
        self.getResource()
        self.getVirtual()

    def getResource(self):
        self.resourcePath = self.response.resourcePath

        self.resourcePath = self.resourcePath[self.resourcePath.rindex('/')+1:]     # http://host:80/virtual/telemetria/status.json -> 'status.json'
        self.virtual = self.resourcePath[:self.resourcePath.rindex('.')]            # status.json -> 'status'

    def getVirtual(self):
        if(self.virtual == "status"):
            self.getStatus()
        else:
            self.response.response404()

    def getStatus(self):
        try:
            file = open('./status.json')
            responseToClient = 'HTTP/1.1 200 OK\r\n' +\
                'Server: Venturini/1.1\r\n' +\
                'Set-Cookie: ' + self.response.operation.getCookies() + '\r\n\r\n'

            self.response.send(responseToClient)
            for line in file:
                self.response.send(line)

        except:
            self.response.response404()