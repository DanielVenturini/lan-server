# -*- coding: ISO-8859-1 -*-

from methods.Virtual import Virtual
from methods.Response import Response

class POST:

    def __init__(self, resourcePath, hash, conn, cookies, query, parent, servers, httpBody):
        self.resourcePath = resourcePath
        self.headerFields = hash
        self.httpBody = httpBody
        self.cookies = cookies
        self.parent = parent
        self.query = query

        self.response = Response(conn, resourcePath, cookies, query, parent, servers, hash)
        self.execute()

    def execute(self):                              # select the def from the resource

        # if is a resource virtual
        if(self.resourcePath.__contains__("/virtual/")):
            print("Contem virtual")
            Virtual(self).start()                   # is not a thread