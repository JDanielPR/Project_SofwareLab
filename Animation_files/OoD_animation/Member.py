import bpy
import math
from abc import ABCMeta, abstractmethod
import BlenderMesh
import imp
import initialization
import setAnimation
import setColor

imp.reload(BlenderMesh)    #Load library
imp.reload(initialization)   #Load library
imp.reload(setAnimation)
imp.reload(setColor)

class Member:
    __metaclass__ = ABCMeta

    @abstractmethod
    def computeLength(self): pass

class horizontalMember(Member):
    def __init__(self , nameOfMember, x1, x2, deformableLength):
        
        self.nameOfMember = nameOfMember
        self.x1 = x1
        self.x2 = x2
        self.deformableLength =  deformableLength
        self.level = int(nameOfMember[1])
        
        self.createDeformablePart(self.deformableLength, self.x2 - self.deformableLength/2)
        self.createNonDeformablePart(self.totalLength() - self.deformableLength, self.x1 + (self.totalLength() - self.deformableLength)/2)
        self.createTag()

    def totalLength(self):
        return math.fabs(self.x2 - self.x1) 
    
    def createDeformablePart(self ,lengthOfElement, xCoordinate):
        self.oE1= BlenderMesh.BlenderElement(str(initialization.static_numberOfElement()), (xCoordinate, 300 * self.level, 0.0), lengthOfElement,(0, math.radians(90), 0),0)
        self.deformPart = self.oE1.get_geometricalObject()
        
    def createNonDeformablePart(self, lengthOfElement, xCoordinate):
        self.oE2 = BlenderMesh.BlenderElement(str(initialization.static_numberOfElement()), (xCoordinate, 300 * self.level, 0.0), lengthOfElement,(0, math.radians(90), 0),1)
        self.nonDeformPart = self.oE2.get_geometricalObject()
    
    def createTag(self):
        self.oT = BlenderMesh.BlenderText(self.nameOfMember,(self.x1 + self.totalLength()/2 - 50, 300 * self.level + 50, 0),(0,0,0))
        self.tag = self.oT.get_geometricalObject()
    
    def move(self, distance, initialFrame, finalFrame):
        setAnimation.setMovement(self.deformPart, initialFrame, finalFrame, distance)
        setAnimation.setMovement(self.nonDeformPart, initialFrame, finalFrame, distance)
        setAnimation.setMovement(self.tag, initialFrame, finalFrame, distance)

    def deform(self, amount, initialFrame, finalFrame):
        setAnimation.setMovement(self.deformPart, initialFrame, finalFrame, (amount/100) * self.deformableLength/2)
        setAnimation.setDeformation(self.deformPart, initialFrame, finalFrame , amount)
        setAnimation.setColor(self.deformPart, initialFrame, finalFrame)
        setAnimation.setMovement(self.tag, initialFrame, finalFrame, (amount/100) * self.deformableLength/2)
        
       
 
   
                
         
        
    
        
        

        
'''	
class inclinedMember(Member):
    def __init__(self , x1, x2, deformableLength, iniLevel, endLevel):

        self.iniLevel = iniLevel
        self.endLevel = endLevel
        self.x1 = x1
        self.x2 = x2
        self.deformableLength =  deformableLength

    def createBlenderMesh(self):
    # Define inclination of a member
        a1 = 0
        a2 = math.radians(90)
        a3 = math.atan2(y2 - y1 , x2 - x1)
        # Define angle of a member on the working plane
        x = x2 - (x2 - x1) / 2
        y = y2 - (y2 - y1) / 2
        z = 0.0
        '''
