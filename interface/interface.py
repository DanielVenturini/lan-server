# -*- coding:ISO-8859-1 -*-

from methods import Operation

def getHeader(title, h1):
    return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\r\n' + \
            '<html>\r\n' + \
            '   <head>\r\n' + \
            '       <meta charset="utf-8"/>\r\n' +\
            '        <meta name="viewport" content="width=device-width, initial-scale=1" />\r\n' +\
            '        <title>' + title + '</title>\r\n' +\
            '        <link rel="stylesheet" href="interface/css/styles.css">\r\n' +\
            '        <link rel="stylesheet" href="interface/css/bootstrap.min.css">\r\n' +\
            '        <script type="text/javascript" src="interface/js/jquery.min.js"></script>\r\n' +\
            '        <script type="text/javascript" src="interface/js/bootstrap.min.js"></script>\r\n' +\
            '    </head>\r\n' +\
            '<body>\r\n' +\
            '    <div class="h1">\r\n' +\
            '        <hr><h1>' + h1 + '</h1><hr>\r\n' +\
            '   </div>\r\n' +\
            '   <div>\r\n'

def getTail():
    return '</div><hr><address>Venturini/1.1 -- ' + Operation.Operation(None, None, None).getCurrentDate() + '</address></body></html>'