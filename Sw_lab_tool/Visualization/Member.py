import bpy
from Visualization import BlenderObject as b
import math as m
from Visualization import setFunction as s
import imp
from Visualization import initialization as i
from Visualization import setColor as c

imp.reload(b)    
imp.reload(i)   
imp.reload(s)
imp.reload(c)
 
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
        '''Creates the object member
    
        Args:
            numberOfFrames:
                float, number of frames that the objects needs for the action
            x1:
                float, location in x of the point one
            x2:
                float, location in x of the point two
            deformableLength:
                float, deformable length
            level1:
                float, level of point one
            level2:
                float, level of point two
            separation:
                float, vertical position of the element
            mass_position:
                float, the absolute position of mass

        Returns: 
            nothing is returned
    
        Raises:
            nothing is raised
        '''
        
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
        self.dX = x2 - x1
        # Rigid length in x direction
        self.rL = self.dX - self.dL
        # Compute initial angle
        self.angle = m.atan(self.dY / self.dX)
        # Compute the real length of element
        self.totalLength = m.sqrt(self.dY * self.dY + self.dX * self.dX)
        # Compute relative deformable length
        self.rDL = self.dL / m.cos(self.angle)
        # Compute relative non deformable length
        self.rRL = self.totalLength - self.rDL
        # Se text size
        self.elementSize = m.fabs(self.sep / 5)
        # Set relative position of mass
        self.rPM = self.mass_position - x1 - 7 * self.elementSize / 12
        
        # Create deformable part
        xd = x1 + self.dL/2
        yd = self.sep * self.l1 + (self.dY - self.rRL * m.sin(self.angle))/2
        zd = 0
        if self.angle != 0:
            # The inclined member have to hidden behind the horizontal ones
            zd = -10 
        oE = b.BlenderObject("dpElement_" + str(i.static_numberOfElement()),
                            (xd , yd , zd),
                            (-self.angle, m.radians(90), 0),
                            (1, self.elementSize  , self.rDL ),
                            c.gray,
                            "member")
        self.deformPart = oE.get_geometricalObject()
        
        # Create rigid part
        xnd = (x2 + x1 + self.dL)/2
        ynd = self.sep * self.l2 - (self.rRL * m.sin(self.angle)) / 2
        znd = 0
        if self.angle != 0:
            znd = -10 
        oE = b.BlenderObject("ndpElement_" + str(i.static_numberOfElement()),
                            (xnd, ynd, znd),
                            (-self.angle, m.radians(90), 0),
                            (1, self.elementSize , self.rRL),
                            c.black,
                            "member")
        self.nonDeformPart = oE.get_geometricalObject()
        
        # Create tag of the member
        xt = (x2 + x1)/2
        yt = self.sep * self.l1 + 3 * self.elementSize / 4
        zt = 10
        oE = b.BlenderObject(nameOfMember,
                           (xt, yt, zt),
                           (0, 0, 0),
                           3 * self.elementSize / 3,
                           c.red,
                           "text")
        self.tag = oE.get_geometricalObject()
        
        # Create left node
        xln = x1
        yln = self.sep * self.l1
        zln = 5
        oE = b.BlenderObject("leftNode_" + nameOfMember,
                            (xln, yln, zln),
                            (0, m.radians(90), 0),
                            (1, self.elementSize * 1.5, self.elementSize / 3),
                            c.dark_gray,
                            "node")
        self.lNode = oE.get_geometricalObject()
        
        # Create right node
        xrn = x2
        yrn = self.sep * self.l2
        zrn = 5
        oE = b.BlenderObject("rightNode_"+ nameOfMember,
                            (xrn, yrn, zrn),
                            (0, m.radians(90), 0),
                            (1, self.elementSize * 1.5, self.elementSize / 3),
                            c.dark_gray,
                            "node")
        self.rNode = oE.get_geometricalObject()  
        
        # Create mass
        if self.mass_position:
            xm = self.mass_position
            ym = self.sep * self.l1 + (xm - x1)  * m.tan(self.angle)
            zm = 0
            oE= b.BlenderObject("m_"+ nameOfMember,
                               (xm, ym, zm),
                               (0, 0, 0),
                               self.elementSize / 2,
                               c.blue,
                               "mass")
            self.mass = oE.get_geometricalObject()
    
    def __repr__(self):
        return self.nameOfMember
    
    def move(self, 
             initialFrame, 
             finalFrame,
             distance):
        '''Define the movement of the element
    
        Args:
            initialFrame:
                integer, the initial frame of the movement
            finalFrame:
                integer, the final frame of the movement
            distance:
                float, the distance of movement

        Returns: 
            nothing is returned
    
        Raises:
            nothing is raised
        '''
        # Move defomable part       
        s.movement(self.deformPart,
                   initialFrame, 
                   finalFrame, 
                   distance)
        # Move rigid part           
        s.movement(self.nonDeformPart,
                   initialFrame, 
                   finalFrame, 
                   distance)
        # Move tag       
        s.movement(self.tag,
                   initialFrame, 
                   finalFrame, 
                   distance)
        # Move left node   
        s.movement(self.lNode,        
                   initialFrame, 
                   finalFrame, 
                   distance)
        # Move right node      
        s.movement(self.rNode,  
                   initialFrame, 
                   finalFrame, 
                   distance)
        # Move mass      
        if self.mass_position:
            s.movement(self.mass, 
                       initialFrame,
                       finalFrame, 
                       distance)
        
    # Method deform element
    def deform(self, 
               initialFrame, 
               finalFrame,
               amount,
               newAmount,
               newAngle,
               oldAngle,
               newDefoLength,
               oldDefoLength,
			   currentStep,
			   numberOfSteps):
        '''Define the movement of the element
    
        Args:
            initialFrame:
                integer, the initial frame of the movement
            finalFrame:
                integer, the final frame of the movement
            amount:
                float, the previous value of the amount of deformation
            newAmount:
                float, the current value of the amount of deformation
            newAngle:
                float, the current angle to rotate
            oldAngle:
                float, the old angle to rotate
            newDefoLength:
                float, the current deformable length
            oldDefoLength:
                float, the old deformable length
            currentStep:
                integer, steps in which the action is
            numberOfSteps:
                integer, number of steps that covers the action

        Returns: 
            nothing is returned
    
        Raises:
            nothing is raised
        '''
        
        # Check if the levels are the same       
        if self.l1 == self.l2:
            # Three actions to animate the deformation of an element
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
                          newAmount)
            # Green color when the deformation starts   
            s.color(self.deformPart,
                    initialFrame,
                    (0,1,0,0.5))
                    
            if numberOfSteps == currentStep:
			    # Go back to the orginal color when the deformation finishes  
                s.color(self.deformPart,
                        finalFrame - 0.1,
                        (0.6,0.6,0.6,0.5))
                        
            # Check if there is a mass             
            if self.mass_position:
                #Condition to check the distance between the mass and the
                #left node
                #If that distance is less that the amount to deform
                #the mass keeps in the left node once it reaches it
                if amount < self.rPM:
                    s.movement(self.mass, 
                               initialFrame, 
                               finalFrame, 
                               amount)
                else:
                    s.movement(self.mass, 
                               initialFrame, 
                               finalFrame, 
                               self.rPM)
        # If the member is inclined the final angle has to be computed
        else:
            # Condition for an 90 degree angle
            if (self.dX - amount) == 0:
                newAngle = m.pi / 2
                newAmount = self.totalLength - self.rDL
                # Red color when the deformation starts   
                s.color(self.deformPart,
                        initialFrame,
                        (1,0,0,0.5))
                        
            # Contition for any other degree        
            else:
                # New relative deformable lenght
                nRDL = newDefoLength /m.cos(newAngle)
                # New relative rigid lenght
                nRRL = self.rL / m.cos(newAngle)
                # Old relative deformable length
                oldrDL = oldDefoLength  / m.cos(oldAngle)
                
                # Check if the element has zero length
                if oldrDL == 0:
                    AmountDef = 1
                else:
                    AmountDef = m.fabs((oldrDL - nRDL) / oldrDL ) 

                if self.rRL == 0:
                    AmountRig = 0
                else:
                    AmountRig = (self.rRL - nRRL) / self.rRL 
                    
            # Distance in y direction that the elements has to move
            offsetDef =-(nRDL* m.sin(newAngle)- oldrDL* m.sin(oldAngle))*0.5
            offsetRig = (nRRL* m.sin(newAngle)- self.rRL* m.sin(oldAngle))*0.5 
            
            # Move the inclined member
            s.movement(self.deformPart,
                       initialFrame, 
                       finalFrame, 
                       amount / 2,
                       offsetDef)

            s.movement(self.nonDeformPart,
                       initialFrame, 
                       finalFrame, 
                       amount,
                       offsetRig)
            
            s.rotation(self.deformPart, 
                       initialFrame, 
                       finalFrame, 
                       -newAngle + oldAngle)

            s.rotation(self.nonDeformPart,
                       initialFrame, 
                       finalFrame, 
                       -newAngle + oldAngle)
                       
            s.deformation(self.deformPart, 
                          initialFrame, 
                          finalFrame,
                          AmountDef )

            s.deformation(self.nonDeformPart, 
                          initialFrame, 
                          finalFrame,
                          AmountRig ) 
                          
            # Red color when the deformation starts   
            s.color(self.deformPart,
                    initialFrame,
                    (1,0,0,0.5))
               
        # Movement of the tag when the element deforms      
        s.movement(self.tag, 
                   initialFrame,
                   finalFrame, 
                   amount / 2)
        
        # Delete the tag at the end of the deformation           
        s.elimination(self.tag,
                      finalFrame - 1,
                      finalFrame)
                      
        # Movement of the rigid element when the element deforms 
        s.movement(self.rNode,
                   initialFrame, 
                   finalFrame, 
                   amount)  
        
        
        