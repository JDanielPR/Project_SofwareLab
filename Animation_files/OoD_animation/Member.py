import bpy
import math
import BlenderMesh
import imp
import initialization
import setAnimation
import setColor

#Load library
imp.reload(BlenderMesh)    
imp.reload(initialization)   
imp.reload(setAnimation)
imp.reload(setColor)

class horizontalMember():
    def __init__(self , nameOfMember, x1, x2, deformableLength, level):
        
        self.nameOfMember = nameOfMember
        self.x1 = x1
        self.x2 = x2
        self.deformableLength =  deformableLength
        self.level = level
        self.distanceBetweenPaths = 50
        
        self.createDeformablePart(self.deformableLength, self.x2 - self.deformableLength/2)
        self.createNonDeformablePart(self.totalLength() - self.deformableLength, self.x1 + (self.totalLength() - self.deformableLength)/2)
        self.createTag()
    
    # Compute length of element
    def totalLength(self):
        return math.fabs(self.x2 - self.x1) 
    
    # Create deformable part
    def createDeformablePart(self ,lengthOfElement, xCoordinate):
        self.oE1= BlenderMesh.BlenderElement(str(initialization.static_numberOfElement()), (xCoordinate, self.distanceBetweenPaths * self.level, 0.0), lengthOfElement,(0, math.radians(90), 0),0)
        self.deformPart = self.oE1.get_geometricalObject()
      
    # Create non deformable part  
    def createNonDeformablePart(self, lengthOfElement, xCoordinate):
        self.oE2 = BlenderMesh.BlenderElement(str(initialization.static_numberOfElement()), (xCoordinate, self.distanceBetweenPaths * self.level, 0.0), lengthOfElement,(0, math.radians(90), 0),1)
        self.nonDeformPart = self.oE2.get_geometricalObject()
    
    # Create red tag in the middle of each element
    def createTag(self):
        self.oT = BlenderMesh.BlenderText(self.nameOfMember,(self.x1 + self.totalLength()/2 - 15, self.distanceBetweenPaths * self.level + 15, 0),(0,0,0),15)
        self.tag = self.oT.get_geometricalObject()
    
    # Move element
    def move(self, distance, initialFrame, finalFrame):
        setAnimation.setMovement(self.deformPart, initialFrame, finalFrame, distance)
        setAnimation.setMovement(self.nonDeformPart, initialFrame, finalFrame, distance)
        setAnimation.setMovement(self.tag, initialFrame, finalFrame, distance)
    
    # Deform element
    def deform(self, amount, initialFrame, finalFrame):
        setAnimation.setMovement(self.deformPart, initialFrame, finalFrame, amount/2)
        setAnimation.setDeformation(self.deformPart, initialFrame, finalFrame , amount/self.deformableLength)
        setAnimation.setColor(self.deformPart, initialFrame)
        setAnimation.setMovement(self.tag, initialFrame, finalFrame, (amount/100) * self.deformableLength/2)
        setAnimation.deleteTag(self.tag, finalFrame -1, finalFrame)
 
   
class inclinedMember():
    def __init__(self , nameOfMember, x1, x2, deformableLength, iniLevel, finalLevel):
        
        self.nameOfMember = nameOfMember
        self.x1 = x1
        self.x2 = x2
        self.deformableLength =  deformableLength
        self.iniLevel = iniLevel
        self.finalLevel = finalLevel
        self.distanceBetweenPaths = 50 *(finalLevel - iniLevel)
        
        self.createDeformablePart(self.deformableLength, self.x2 - self.deformableLength/2)
        
    # Compute the real length of element
    def totalLength(self):
        return math.sqrt(self.distanceBetweenPaths * self.distanceBetweenPaths + (self.x2 - self.x1)*(self.x2 - self.x1))
    
    # Create deformable part
    def createDeformablePart(self ,lengthOfElement, xCoordinate):
        self.oE1= BlenderMesh.BlenderElement(str(initialization.static_numberOfElement()), (xCoordinate, 50 * (self.finalLevel) - self.distanceBetweenPaths * 0.5, - 10), self.totalLength() ,(-math.atan(self.distanceBetweenPaths/(self.x2 - self.x1)), math.radians(90), 0),0)
        self.deformPart = self.oE1.get_geometricalObject()
    
        
    
        
        