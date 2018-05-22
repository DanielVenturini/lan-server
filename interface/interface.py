# -*- coding:ISO-8859-1 -*-

from methods import Operation

def getHeader(title, h1, parent, redirect=''):
    return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\r\n' + \
            '<html>\r\n' + \
            '   <head>\r\n' + \
            '       <meta charset="utf-8"/>\r\n' +\
            '        <meta name="viewport" content="width=device-width, initial-scale=1" />\r\n' +\
            '        ' + redirect + '\r\n' +\
            '        <title>' + title + '</title>\r\n' +\
            '        <link rel="stylesheet" href="/interface/css/styles.css">\r\n' +\
            '        <link rel="stylesheet" href="/interface/css/bootstrap.min.css">\r\n' +\
            '        <script type="text/javascript" src="/interface/js/jquery.min.js"></script>\r\n' +\
            '        <script type="text/javascript" src="/interface/js/bootstrap.min.js"></script>\r\n' +\
            '    </head>\r\n' +\
            '<body class="texto">\r\n' +\
            '    <div class="h1">\r\n' +\
            '        <hr><h1>' + h1 + '</h1><hr>\r\n' +\
            '   </div>\r\n' +\
            '   <table cellspacing="10">\r\n' + \
            '       <tr><td><img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4gQBEyAn9IpdbAAAA5pJREFUOMu9lH9sU1UUx7/v3verP7a+dnNhrIrTbZ3QzUUzdVERJf4BOBSN0xiMi8TsD4gY/yDOheg/Jhg1ISYydSQYFCWAGiGoIxRhY2PJgswOuq2zY4xuXelr2WhLu7bvXf94rUbDH1s0nuQk59x7z+fec3POAW4hqzb64Fp/Me91UvxXsrp1/LP2znDU4f7U9a9A7qcvPd/epQZ/vqSx0+M6a3jyw47FxpKVzcN/OvWbRpR12y73v7PTdWjN6pIKSSJgDJCLazY+9fJuecXa30yktk8onO9nDBUN7/0NyBWMps3+91tedG6tvNNkESnAE0CkgECBuVgGBPoCBbsRnFlQewbm/F98F9yDkUdPAECZayuujX1iAJs2+6uqqq2965uXLZN5DoQYkIJKFJB4Q2UBsEhAsQm4Gszgyx/Cwe4zM62D3z7kef0cw8dNHLiWt4O7n2up2E45gBJDBQoI+ReKfB4qGECZ5sGikdloSGPb3vq1q/fAA21xxkDFsi2mdJp/oXy5CSYZIPgLTImRusAblxS+QaTGmqYDiQzhSlbcdv9woE7f8aq7h9rvamOqmmkLBFLUZjOj1EHAU4ByAJ+HJG8avkjzGfCAzAMLGqAmgLhGkMooTd4zfXvpjTSL8lx2FETZMBdnQkTVodhk2G0A4QCOAb5pYGYe8E8zjE0xeAM6pkIMNiuHpMYhFNNxLZxiF73eQ7xVTGKy/7XDk8DJ1Lpf9nGobNZ0naixIjS4BMgW4NzZYDadjF4pVqwWu8OqSKZiUyIr4fyPOZSXEghWHamUxhFOo3ws8FWhcq77fnp8U9j/Ul114/ZjdkftHX1DGswij+nJievdXY81io61mkCzdnNRUYPz3o4PHllTVxOhMrJhhkQix5h+M0f+UegsGvjaO3Dwwaoj+z3tgd9nk45yCkp1AFjIxDzxZKRnKjJx/CiVlAMjvgiCV+MglECWLGDgdP5W7VNa3Zr1n3p2l/8U9p71fL9/fupwAEDK2D3BPfxKpdvpNHfMz2UxdCEM5+02UEqgaxnGLbJFKQANALbsmv2orEx+M6pmcHkiAUWxwHVPKQYHJtPdnXfXkEUCtYJhd4irGGOIJ3JQ7GasdJdgNhRH/7Gd+wCE+KVOojFfUryvsQT19VbojODCeRWeg2/siQe/2QEgt2SgKOFKfD6L4fHh6OjQYK/v9Lufg6knAWSXPCernjgOiLVWoOgZAMvxf8gfuVRj87BbYIEAAAAASUVORK5CYII="></td><td><a href=' + parent + '>Parent Directory</a></td>\r\n' + \
            '   </table>\r\n' + \
            '   <div>\r\n'

def getTail():
    return '</div><hr><address>Venturini/1.1 -- ' + Operation.Operation(None, None, None).getCurrentDate() + '</address></body></html>'

def getPageFromFeedback(address):
    page = getHeader('Feedback', 'Thanks for feedback. You\'ll be redirect to home in 5 segs.', '.' , '<meta http-equiv="refresh" content="5; url='+address+'">')
    page += getTail()

    return page
