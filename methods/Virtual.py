# -*- coding:ISO-8859-1 -*0

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
       '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' + \
       '<html><head>' + \
       '<title>Status</title>' + \
       '</head><body style="background-color: AliceBlue;">' + \
       '<div style="background-color:yellow">\r\n' + \
       '<hr><h1>Telemetria Status</h1><hr>' + \
       '</div><hr>\r\n' + \
       '<p> number of requests met: ' + str(self.get.reqCount) + ' </p>\r\n' + \
       '<p> server up time: ' + self.get.upTime + ' </p>\r\n' +\
       '<p> conected servers: ' + self.conectedServers() + '</p>' +\
       '<table cellspacing="10">\r\n' + \
       '<tr><td><img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4gQBEyAn9IpdbAAAA5pJREFUOMu9lH9sU1UUx7/v3verP7a+dnNhrIrTbZ3QzUUzdVERJf4BOBSN0xiMi8TsD4gY/yDOheg/Jhg1ISYydSQYFCWAGiGoIxRhY2PJgswOuq2zY4xuXelr2WhLu7bvXf94rUbDH1s0nuQk59x7z+fec3POAW4hqzb64Fp/Me91UvxXsrp1/LP2znDU4f7U9a9A7qcvPd/epQZ/vqSx0+M6a3jyw47FxpKVzcN/OvWbRpR12y73v7PTdWjN6pIKSSJgDJCLazY+9fJuecXa30yktk8onO9nDBUN7/0NyBWMps3+91tedG6tvNNkESnAE0CkgECBuVgGBPoCBbsRnFlQewbm/F98F9yDkUdPAECZayuujX1iAJs2+6uqqq2965uXLZN5DoQYkIJKFJB4Q2UBsEhAsQm4Gszgyx/Cwe4zM62D3z7kef0cw8dNHLiWt4O7n2up2E45gBJDBQoI+ReKfB4qGECZ5sGikdloSGPb3vq1q/fAA21xxkDFsi2mdJp/oXy5CSYZIPgLTImRusAblxS+QaTGmqYDiQzhSlbcdv9woE7f8aq7h9rvamOqmmkLBFLUZjOj1EHAU4ByAJ+HJG8avkjzGfCAzAMLGqAmgLhGkMooTd4zfXvpjTSL8lx2FETZMBdnQkTVodhk2G0A4QCOAb5pYGYe8E8zjE0xeAM6pkIMNiuHpMYhFNNxLZxiF73eQ7xVTGKy/7XDk8DJ1Lpf9nGobNZ0naixIjS4BMgW4NzZYDadjF4pVqwWu8OqSKZiUyIr4fyPOZSXEghWHamUxhFOo3ws8FWhcq77fnp8U9j/Ul114/ZjdkftHX1DGswij+nJievdXY81io61mkCzdnNRUYPz3o4PHllTVxOhMrJhhkQix5h+M0f+UegsGvjaO3Dwwaoj+z3tgd9nk45yCkp1AFjIxDzxZKRnKjJx/CiVlAMjvgiCV+MglECWLGDgdP5W7VNa3Zr1n3p2l/8U9p71fL9/fupwAEDK2D3BPfxKpdvpNHfMz2UxdCEM5+02UEqgaxnGLbJFKQANALbsmv2orEx+M6pmcHkiAUWxwHVPKQYHJtPdnXfXkEUCtYJhd4irGGOIJ3JQ7GasdJdgNhRH/7Gd+wCE+KVOojFfUryvsQT19VbojODCeRWeg2/siQe/2QEgt2SgKOFKfD6L4fHh6OjQYK/v9Lufg6knAWSXPCernjgOiLVWoOgZAMvxf8gfuVRj87BbYIEAAAAASUVORK5CYII="></td><td><a href=/>Parent Directory</a></td>\r\n' + \
       '</table>\r\n' + \
       '<hr>' + \
       '<address>Venturini/1.1 -- ' + self.get.operation.getCurrentDate() + '</address>' + \
       '</body></html>'

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