# -*- coding: ISO-8859-1 -*-

class CommonGatewayInterface:

    def __init__(self, resourcePath, conn, headerFields):
        print("TENTANDO ACESSAR UM AQUIVO COM A EXTENSAO PONTO DIM")
        self.headerFields = headerFields
        self.conn = conn
        self.resourcePath = resourcePath
        self.file = open(self.resourcePath, "r")

        self.readFile()         # get only the CGI
        self.joinCGI()
        self.solveInstructions()
        print(self.dyn)

    def readFile(self):
        lines = self.file.readlines()
        self.dyn = ""

        lastI = 0
        for i in range(0, len(lines)):
            lastI = i
            if(lines[i].find("<%") != -1):
                if (lines[i].find("%>") != -1):
                    self.dyn = lines[i][lines[i].find("<%"):lines[i].find("%>")]
                    return
                else:
                    self.dyn = lines[i][lines[i].find("<%"):]
                    break

        lastI += 1
        for i in range(lastI, len(lines)):
            if (lines[i].find("%>") != -1):
                self.dyn += lines[i]
                break
            else:
                self.dyn += lines[i][:lines[i].find("%>")]

    def joinCGI(self):
        # remove all break line
        self.dyn = self.dyn.replace("\r", "")
        self.dyn = self.dyn.replace("\n", "")
        # remove all space in the string
        self.dyn = self.dyn.replace(" ", "")

        self.dyn = self.dyn[2:-3]           # remove the '<%' and ';%>'
        self.dyn = self.dyn.split(";")      # separe the instructions

    def solveInstructions(self):

        for i in range(0, len(self.dyn)):
            if(self.dyn[i][0:self.dyn[i].index("(")] == "getHeaderField"):
                print("Requerido o " + self.dyn[i][self.dyn[i].index("(")+2:-2])
            elif(self.dyn[i][0:self.dyn[i].index("(")] == "date"):
                print("Requerido o " + self.dyn[i][self.dyn[i].index("(")+2:-2])