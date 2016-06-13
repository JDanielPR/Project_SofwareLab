import bpy
from abc import ABCMeta, abstractmethod
import math
from math import pi
import imp
import random


class ReadInput:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getInformation(self): pass

class ReadTxt(ReadInput):
    def __init__(self , filename):
        self.file = open(filename, "r") 
        
    def getInformation(self):
        numberOfNodes = int(self.file.readline())
        numberOfElements = int(self.file.readline())
        numberOfHorizontalLevels =int(self.file.readline())
    
        genericList= []
        nodes = []
        elements = []
    
        genericList= self.file.read().split()
        self.file.close()
        k = 0
        for i in range(numberOfNodes + numberOfElements ):
            if i < numberOfNodes:
                nodes.append([])
                for j in range(3*(i+1)-3,3*(i+1)):
                    nodes[i].append(float(genericList[j])) 
                k =  3*(i+1)
            else:
                elements.append([])
                for j in range(k, k + 7):
                    elements[i - numberOfNodes].append(float(genericList[j]))
                k = k + 7   
            
        return (nodes, elements , numberOfNodes, numberOfElements, numberOfHorizontalLevels)
  