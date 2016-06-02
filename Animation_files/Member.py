import bpy
from abc import ABCMeta, abstractmethod
import math
from math import pi

class Member():
    def __init__(self , name , iniLevel, endLevel, x1, x2, weight , deformableLength, defoRatio, maximumForce, materialProperty , orderOfDeformation):
              
        self.name = name
        self.iniLevel = iniLevel
        self.endLevel = endLevel
        self.x1 = x1
        self.x2 = x2
        self.weight = weight
        self.deformableLength = deformableLength 
        self.defoRatio =  defoRatio
        self.maximumForce =  maximumForce
        self.materialProperty =  materialProperty
        self.orderOfDeformation = orderOfDeformation
        self.totalLength = 0.0
        self.angle = 0.0

    def get_name(self):
        return self.name
		
    def get_iniLevel(self):
        return self.iniLevel
		
    def get_endLevel(self):
        return self.endLevel
		
    def get_x1(self):
        return self.x1
		
    def get_x2(self):
        return self.x2
		
    def get_weight(self):
        return self.weight
		
    def get_deformableLength(self):
        if self.iniLevel != self.endLevel:
            aux = 0.0
            self.angle = math.atan2(300, deformableLength)
            if self.angle != 0:
                aux = self.totalLength() * math.sqrt(1 + 1/(math.tan(self.angle ))**2)   
            return aux
        else:
            return self.deformableLength
    
    def get_nondeformableLength(self):
            return self.totalLength() - self.get_deformableLength()
                  
    def get_deformationRatio(self):
        return self.deformationRatio 
		
    def get_maximumForce (self):
        return self.maximumForce 
		
    def get_materialProperty(self):
        return self.materialProperty 
		
    def get_orderOfDeformation(self):
        return self.orderOfDeformation
    
    def totalLength():
        if self.iniLevel != self.endLevel:
            return math.sqrt((self.x2() - self.x1()) ** 2 + 300 ** 2)   
        else:
            return math.fabs(self.x2 - self.x1)
    
	
    