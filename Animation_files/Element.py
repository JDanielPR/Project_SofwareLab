import math  #Module for math operations
import bpy   #Module for blender
import imp
import setColor
import Node
import BlenderMesh
import Puntos

imp.reload(setColor)         #Load library
imp.reload(Node)             #Load library
imp.reload(BlenderMesh)    #Load library
imp.reload(Puntos)         #Load library
        

class Element():
    def __init__(self , numberOfElement  , nodeA , nodeB  , levelOfNodeA, levelOfNodeB, elementType, deformationPercentage, orderOfDeformation):
        self.numberOfElement = numberOfElement              # Every element has a unique number
        self.nodeA = nodeA                                  # First object node
        self.nodeB = nodeB                                  # Second object node
        self.levelOfNodeA = levelOfNodeA                    # Starting level of element
        self.levelOfNodeB = levelOfNodeB                    # Final level of element
        self.elementType = elementType                      # 0 if it deforms, 1 if it is rigid, 2 if it is a gap
        self.deformationPercentage = deformationPercentage  # From 0 to 100 , it is the percentage of the deformability of the elements which deforms
        self.orderOfDeformation = orderOfDeformation        # Unique number in each level in which it will deform, starting with number 1
        self.blenderElement = []      
        self.blenderElement2 = []                       # This variable stores the physical object member rectangle for the animation
        self.tag =[]
        # Define coordinates of a member 
        xi = self.nodeA.get_xCoordinate()
        yi = self.nodeA.get_yCoordinate() 
        xj = self.nodeB.get_xCoordinate()
        yj = self.nodeB.get_yCoordinate()
        # Define inclination of a member
        a1 = 0
        a2 = math.radians(90)
        a3 = math.atan2(yj - yi , xj - xi)
        # Define angle of a member on the working plane
        x = xj - (xj - xi) / 2
        y = yj - (yj - yi) / 2
        z = 0.0
        # Create ether a physical element or a gap
        if self.elementType != 2:
            
        
            oE = BlenderMesh.BlenderElement(str(self.numberOfElement ), (x, y, z), self.computeLength(),(a1, a2, a3),self.get_elementType())
            self.blenderElement = oE.get_geometricalObject()
            selectedObject = bpy.context.selected_objects
            # Assign color depending whether is a deformable element or non deformable element
            if self.get_elementType() == 1:   # Condition for rigid elements
                setColor.setMaterial(bpy.context.object, setColor.black) # Elements in black are rigid elements
            else:                             # Condition for deformable elements
                setColor.setMaterial(bpy.context.object, setColor.white) # Elements in white are deformable elements
                #oT = BlenderMesh.BlenderText(str(self.numberOfElement),(x + self.computeLength()/2 - 50, 300 * levelOfNodeA + 50, 0),(0,0,0))
                #self.tag = oT.get_geometricalObject()  
            bpy.ops.object.shade_smooth() 
        else:
            oE = BlenderMesh.BlenderGap(str(self.numberOfElement ), (x, y, z), self.computeLength(),(a1, a2, a3))
            self.blenderElement = oE.get_geometricalObject()
        
        #node1 = Puntos.Puntos(self.nodeA.get_nodeNumber(), xi, yi)
        #self.blenderElement2 = node1.get_blenderElement()
        
    # Definition of functions to retrieve information about the element    
    def get_numberOfElement(self):
        return self.numberOfElement 
		
    def get_nodeA(self):
        return self.nodeA.get_nodeNumber()
		
    def get_nodeB(self):
        return self.nodeB.get_nodeNumber()
		
    def get_levelOfNodeA (self):
        return self.levelOfNodeA 
		
    def get_levelOfNodeB(self):
        return self.levelOfNodeB
		
    def get_elementType(self):
        return self.elementType
		
    def get_deformationPercentage(self):
        return self.deformationPercentage
		
    def get_numberOfElementInLoadpath(self):
        return self.numberOfElementInLoadpath
		
    def get_blenderElement(self):
        return self.blenderElement    # Return the physical element rectangle of the element
    

    def get_orderOfDeformation(self):
        return self.orderOfDeformation 
		
    def computeLength(self):
        return math.sqrt((self.nodeA.get_xCoordinate() - self.nodeB.get_xCoordinate()) ** 2 + (self.nodeA.get_yCoordinate() - self.nodeB.get_yCoordinate()) ** 2)   