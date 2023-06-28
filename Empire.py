import os
import re

class Empire:
    def __init__(self, s:str):
        self.fulltxt = s
        self.fulltxtList = s.split('\n')
        self.name = self.getNameFromtxt()

    def getNameFromtxt(self):
        indexOfApo = [m.start() for m in re.finditer('"', self.fulltxtList[0])]
        return self.fulltxtList[0][indexOfApo[0]+1:indexOfApo[1]]

    def __str__(self):
        return self.name

    def changeName(self, newName:str):
        self.fulltxt = self.fulltxt.replace(self.name, newName)
        self.fulltxtList = self.fulltxt.split('\n')
        self.name = newName