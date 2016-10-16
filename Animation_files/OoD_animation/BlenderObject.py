import bpy   #Module for blender
import imp   #Module to import libraries
import Color #Module that contains the color features

imp.reload(Color)

'''
This class can provide three diferent object
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
        # Properties of object member
        if self.type == "node" or self.type == "member":
            # Type of blender object 
            self.object = meshElement 
            self.object(location = self.location, 
                        rotation = self.rotation ) 
            bpy.context.object.dimensions = self.dimension 
            self.obj = bpy.context.object
        # Properties of object mass
        elif self.type == "mass":
            self.object = meshMass 
            self.object(location = self.location, 
                        size = self.dimension) 
            self.obj = bpy.context.object
        # Properties of object text
        elif self.type == "text":
            self.object = meshText 
            self.object(location = self.location, 
                        rotation = self.rotation ) 
            self.obj = bpy.context.object  
            self.obj.data.body = self.name
            self.obj.data.size = self.dimension  
        # Define name of object  
        self.obj.name = self.name  
        # Define color of object  
        Color.setColor(self.obj, 
                       self.color)   
        return self.obj
    