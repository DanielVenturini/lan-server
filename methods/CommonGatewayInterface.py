# -*- coding: ISO-8859-1 -*-

class CommonGatewayInterface:

    def __init__(self, resourcePath):
        self.resourcePath = resourcePath
        self.file = open(self.resourcePath, "r")

        self.readFile()

    def readFile(self):
        lines = self.file.readlines()
        init, end = -1, -1
        self.dym = ""

        lastI = 0
        for i in range(0, len(lines)):
            lastI = i
            if(lines[i].find("<%") != -1):
                if (lines[i].find("%>") != -1):
                    self.dym = lines[i][lines[i].find("<%"):lines[i].find("%>")]
                    return
                else:
                    self.dym = lines[i][lines[i].find("<%"):]
                    break

        lastI += 1
        for i in range(lastI, len(lines)):
            if (lines[i].find("%>") != -1):
                self.dym += lines[i]
            else:
                self.dym += lines[i][:lines[i].find("%>")]