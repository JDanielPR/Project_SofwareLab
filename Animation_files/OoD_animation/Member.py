import bpy
import BlenderObject as b
import math as m
import settingFunction as s
import imp
import initialization as i
import Color

#Load library
imp.reload(b)    
imp.reload(i)   
imp.reload(s)
imp.reload(Color)

'''
Class member
The objects of this class are Blender Mesh
with all the characteristics of a member such as
mass, nodes, slanting, tag, deformable part
and non deformable part
'''  
class generalMember():
    def __init__(self, 
                 nameOfMember, 
                 x1, 
                 x2, 
                 deformableLength, 
                 level1, 
                 level2, 
                 separation,
                 mass_position = 0 ):
        
        # Name of the element as whole
        self.nameOfMember = nameOfMember
        # Coordinate of left node
        self.x1 = x1
        # Coordinate of right node
        self.x2 = x2
        # Deformable length in x direction
        self.dL = deformableLength
        # Level of left node
        self.l1 = level1
        # Level of right node
        self.l2 = level2
        # Separation between horizontal loadpaths 
        self.sep = - separation
        # Position of the mass
        self.mass_position = mass_position 
        # Delta Y : Vertical distance between level2 and level1
        self.dY = self.sep * (self.l2 - self.l1)
        # Delta X : Distance between x2 and x1
        self.dX = self.x2 - self.x1
        # Compute initial angle
        self.angle = m.atan(self.dY/self.dX)
        # Compute the real length of element
        self.totalLength = m.sqrt(self.dY * self.dY + self.dX * self.dX)
        # Compute relative deformable length
        self.rDL = self.dL / m.cos(self.angle)
        # Compute relative non deformable length
        self.rRL = self.totalLength - self.rDL
        # Text size
        self.elementSize = m.fabs(self.sep / 5)
        
        # Create deformable part
        xd = self.x1 + self.dL/2
        yd = self.sep * self.l1 + (self.dY - self.rRL * m.sin(self.angle))/2
        zd = 0
        if self.angle != 0:
            zd = -10 
        oE = b.BlenderObject("dpElement_" + str(i.static_numberOfElement()),
                            (xd , yd , zd),
                            (-self.angle, m.radians(90), 0),
                            (1, self.elementSize, self.rDL ),
                            Color.gray,
                            "member")
        self.deformPart = oE.get_geometricalObject()
        
        # Create rigid part
        xnd = (self.x2 + self.x1 + self.dL)/2
        ynd = self.sep * self.l2 - (self.rRL * m.sin(self.angle)) / 2
        znd = 0
        if self.angle != 0:
            znd = -10 
        oE = b.BlenderObject("ndpElement_" + str(i.static_numberOfElement()),
                            (xnd, ynd, znd),
                            (-self.angle, m.radians(90), 0),
                            (1, self.elementSize, self.rRL),
                            Color.black,
                            "member")
        self.nonDeformPart = oE.get_geometricalObject()
        
        # Create tag of the member
        xt = (self.x2 + self.x1)/2
        yt = self.sep * self.l1 + self.elementSize / 2
        zt = 10
        oE = b.BlenderObject(self.nameOfMember,
                           (xt, yt, zt),
                           (0, 0, 0),
                           self.elementSize,
                           Color.red,
                           "text")
        self.tag = oE.get_geometricalObject()
        
        # Create left node
        xln = self.x1
        yln = self.sep * self.l1
        zln = 10
        oE = b.BlenderObject("leftNode_" + self.nameOfMember,
                            (xln, yln, zln),
                            (0, m.radians(90), 0),
                            (1, self.elementSize * 1.5, self.elementSize / 3),
                            Color.dark_gray,
                            "node")
        self.lNode = oE.get_geometricalObject()
        
        # Create right node
        xrn = self.x2
        yrn = self.sep * self.l2
        zrn = 10
        oE = b.BlenderObject("rightNode_"+ self.nameOfMember,
                            (xrn, yrn, zrn),
                            (0, m.radians(90), 0),
                            (1, self.elementSize * 1.5, self.elementSize / 3),
                            Color.dark_gray,
                            "node")
        self.rNode = oE.get_geometricalObject()  
        
        # Create mass
        if self.mass_position:
            xm = self.mass_position
            ym = self.sep * self.l2 - (self.rDL * m.sin(self.angle))/2
            zm = 0
            oE= b.BlenderObject("m_"+ self.nameOfMember,
                               (xm, ym, zm),
                               (0, 0, 0),
                               self.elementSize / 2,
                               Color.blue,
                               "mass")
            self.mass = oE.get_geometricalObject()
  
    # Move element
    def move(self, 
             distance, 
             initialFrame, 
             finalFrame):
                 
        s.movement(self.deformPart,
                   initialFrame, 
                   finalFrame, 
                   distance)
                   
        s.movement(self.nonDeformPart,
                   initialFrame, 
                   finalFrame, 
                   distance)
                   
        s.movement(self.tag,
                   initialFrame, 
                   finalFrame, 
                   distance)
                   
        s.movement(self.lNode,        
                   initialFrame, 
                   finalFrame, 
                   distance)
                   
        s.movement(self.rNode,  
                   initialFrame, 
                   finalFrame, 
                   distance)
                   
        if self.mass_position:
            s.movement(self.mass, 
                       initialFrame,
                       finalFrame, 
                       distance)
        
    # Deform element
    def deform(self, 
               amount, 
               initialFrame, 
               finalFrame):
                   
        if self.l1 == self.l2:
            s.movement(self.deformPart,
                       initialFrame, 
                       finalFrame, 
                       amount / 2)
                       
            s.movement(self.nonDeformPart,
                       initialFrame, 
                       finalFrame, 
                       amount)
                       
            s.deformation(self.deformPart,
                          initialFrame, 
                          finalFrame, 
                          amount/self.dL)
        else:
            # Compute final angle
            if (self.dX - amount) == 0:
                newAngle = m.pi / 2
            else:
                newAngle = m.atan(self.dY/(self.dX - amount))
            offsetX = self.rRL * (m.cos(self.angle) - m.cos(newAngle)) / 2
            offsetY = self.rDL * (m.sin(self.angle) - m.sin(newAngle)) / 2
            newAmount = self.totalLength - ((self.dX - amount)/m.cos(newAngle)) 
            s.movement(self.deformPart,
                       initialFrame, 
                       finalFrame, 
                       amount / 2 - offsetX,
                       offsetY)
                       
            s.rotation(self.deformPart, 
                       initialFrame, 
                       finalFrame, 
                       newAngle - self.angle)
                       
            s.movement(self.nonDeformPart,
                       initialFrame, 
                       finalFrame, 
                       amount - offsetX,
                       offsetY)
                       
            s.rotation(self.nonDeformPart,
                       initialFrame, 
                       finalFrame, 
                       newAngle - self.angle)
            
            s.deformation(self.deformPart, 
                          initialFrame, 
                          finalFrame,
                          newAmount / self.rDL)
            
        s.color(self.deformPart,
                initialFrame)
                
        s.movement(self.tag, 
                   initialFrame,
                   finalFrame, 
                   amount / 2)
                   
        s.movement(self.rNode,
                   initialFrame, 
                   finalFrame, 
                   amount)  
                   
        if self.mass_position:
            s.movement(self.mass, 
                       initialFrame, 
                       finalFrame, 
                       amount, 
                       self.angle)
        
        