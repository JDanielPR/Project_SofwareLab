import Node
import myHeader
import imp
import colores
import math
import bpy   #Module for blender

imp.reload(colores)    #Load library
imp.reload(Node)       #Load library
imp.reload(myHeader)   #Load library

class Element():
    def __init__(self , num  , nodeA , nodeB  , startingLoadpath , finalLoadpath, elementType, deformation, orderOfDeformation):
        self.num = num
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.startingLoadpath = startingLoadpath
        self.finalLoadpath = finalLoadpath
        self.elementType = elementType
        self.deformation = deformation
        self.orderOfDeformation = orderOfDeformation 
        self.member= []
        
        # Define coordinates of a member 
        xi = self.nodeA.get_x()
        yi = self.nodeA.get_y() 
        xj = self.nodeB.get_x()
        yj = self.nodeB.get_y()
        # Define inclination of a member
        a1 = 0
        a2 = math.radians(90)
        a3 = math.atan2(yj - yi , xj - xi)
        # Define angle of a member on the working plane
        x = xj - (xj - xi) / 2
        y = yj - (yj - yi) / 2
        z = 0.0
        # Create element
        if self.elementType != 2:
            self.member = myHeader.createMember(str(self.num), (x, y, z), self.calcLength(),(a1, a2, a3),self.get_elementType())
            selectedObject = bpy.context.selected_objects
            # Clasify two list, one for rigid elements and the other for deformable elements
            if self.get_elementType() == 1:   
                colores.setMaterial(bpy.context.object, myHeader.black)
            else:  
                colores.setMaterial(bpy.context.object, myHeader.white)   
            bpy.ops.object.shade_smooth() 
        else:
            self.member = myHeader.createGap(str(self.num), (x, y, z), self.calcLength(),(a1, a2, a3),self.get_elementType())
        
    def get_num(self):
        return self.num
		
    def get_A(self):
        return self.nodeA.get_num()
		
    def get_B(self):
        return self.nodeB.get_num()
		
    def get_startingLoadpath (self):
        return self.startingLoadpath
		
    def get_finalLoadpath (self):
        return self.finalLoadpath 
		
    def get_elementType(self):
        return self.elementType
		
    def get_deformation(self):
        return self.deformation
		
    def get_numberOfElementInLoadpath(self):
        return self.numberOfElementInLoadpath
		
    def get_member(self):
        return self.member
		
    def get_orderOfDeformation(self):
        return self.orderOfDeformation 
		
    def set_orderOfDeformation(self, orderOfDeformation ):
        self.orderOfDeformation = orderOfDeformation 
		
    def calcLength(self):
        return math.sqrt((self.nodeA.get_x() - self.nodeB.get_x()) ** 2 + (self.nodeA.get_y() - self.nodeB.get_y()) ** 2)   