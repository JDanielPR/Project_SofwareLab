import bpy           #Module for blender
import imp           #Module to import libraries
from Visualization import setColor as c #Contains the color features

imp.reload(c)

'''
This class can provide three diferent objects
Object 1 == object member (Represented by a blender cube)
Object 2 == object mass (Represented by a blender sphere)
Object 3 == object text (Represented by a blender text)
'''
# List of Blender elements
# Blender Mesh cube used to represent a member or a node
meshElement = bpy.ops.mesh.primitive_cube_add
# Blender Mesh sphere used to represent a mass
meshMass = bpy.ops.mesh.primitive_uv_sphere_add
# Blender text used to represent the tag of a member
meshText = bpy.ops.object.text_add

class BlenderObject():
    def __init__(self , 
                 name, 
                 location, 
                 rotation, 
                 dimension, 
                 color, 
                 type):
        '''Set the color of an object
    
        Args:
            name:
                string, object name
            location:
                coordinate of the object
            rotation:
                define rotation
            dimension:
                float, size of the object
            color
            type:
                type of blender object according to the definition above
    
        Returns: 
            nothing is returned
    
        Raises:
            nothing is raised
        '''
        # Name of element            
        self.name = name  
        # Location          
        self.location  = location
        # Rotation
        self.rotation  = rotation  
        # Dimension  
        self.dimension = dimension  
        # Color 
        self.color     = color   
        # 1 => member or node / 2 => mass / 3 => text         
        self.type      = type   

    def get_geometricalObject(self):
        '''Define the object in Blender
    
        Args:
            nothing is taken
    
        Returns: 
            nothing is returned
    
        Raises:
            nothing is raised
        '''  
        # Properties of object element
        if self.type == "node" or self.type == "member":
            # Assign "mesh Element"  to object
            self.object = meshElement 
            self.object(location = self.location, 
                        rotation = self.rotation ) 
            bpy.context.object.dimensions = self.dimension 
            # Assign the just created object to another variable
            self.obj = bpy.context.object
        # Properties of object mass
        elif self.type == "mass":
            # Assign "mesh Mass"  to object
            self.object = meshMass 
            self.object(location = self.location, 
                        size = self.dimension) 
            # Assign the just created object to another variable
            self.obj = bpy.context.object
        # Properties of object text
        elif self.type == "text":
            # Assign "mesh Text"  to object
            self.object = meshText 
            self.object(location = self.location, 
                        rotation = self.rotation ) 
            self.obj = bpy.context.object  
            self.obj.data.body = self.name
            # Assign the just created object to another variable
            self.obj.data.size = self.dimension 
        # Define name of object  
        self.obj.name = self.name  
        # Define color of object  
        c.setColor(self.obj, self.color)   
        return self.obj
    