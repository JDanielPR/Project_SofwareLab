import bpy   #Module for blender
from bpy import context
import setColor
import imp

imp.reload(setColor)         #Load library

class BlenderElement():
    def __init__(self , name, loc, length, rot,type):
        self.name = name        # Name of element
        self.loc  = loc         # Location
        self.length = length    # Length
        self.rot = rot          # Rotation
        self.type = type        # Deformable or non deformable
        
    def get_geometricalObject(self):
        #Create blender element
        cubeobject = bpy.ops.mesh.primitive_cube_add
        cubeobject (location = self.loc, rotation = self.rot ) 
        bpy.context.object.dimensions = 1, 10, self.length       
        self.ob = bpy.context.object
        self.ob.name = "Ob" + self.name 
        # Elements in gray are non-rigid elements
        if self.type == 0:  
            setColor.setMaterial(self.ob, setColor.gray)  
        # Elements in black are rigid elements
        elif self.type == 1:
            setColor.setMaterial(self.ob, setColor.black) 
        return self.ob

class BlenderText():
    def __init__(self , name, loc, rot, size):
        self.name = name  # Name of element
        self.loc = loc    # Location of tag
        self.rot =rot     # Rotation of tag
        self.size = size  # Size of tag
    
    def get_geometricalObject(self):
        bpy.ops.object.text_add( location = self.loc, rotation = self.rot)
        self.ob = bpy.context.object
        self.ob.name = self.name
        self.ob.data.body = self.name
        self.ob.data.size = self.size
        setColor.setMaterial(bpy.context.object, setColor.red) 
        return self.ob