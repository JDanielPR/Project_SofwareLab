import bpy   #Module for blender
import math
from bpy import context
import setColor
from abc import ABCMeta, abstractmethod
import imp

imp.reload(setColor)         #Load library
#Define variables for primitive shapes
cubeobject = bpy.ops.mesh.primitive_cube_add
sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
cylinderobject = bpy.ops.mesh.primitive_cylinder_add

class BlenderMesh:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_geometricalObject(self): pass

class BlenderElement(BlenderMesh):
    def __init__(self , name, loc, length, rot,type):
        self.name = name
        self.loc  = loc
        self.length = length
        self.rot = rot
        self.type = type
        
    def get_geometricalObject(self):
        cubeobject (location = self.loc, rotation = self.rot ) 
        bpy.context.object.dimensions = 1, 10, self.length       
        self.ob = bpy.context.object
        self.ob.name = "o" + self.name 
        if self.type == 0:  
            setColor.setMaterial(self.ob, setColor.white) # Elements in black are rigid elements
        elif self.type == 1:
            setColor.setMaterial(self.ob, setColor.black) # Elements in black are rigid elements
        return self.ob

class BlenderText(BlenderMesh):
    def __init__(self , name, loc, rot):
        self.name = name
        self.loc = loc
        self.rot =rot
    
    def get_geometricalObject(self):
        bpy.ops.object.text_add( location = self.loc, rotation = self.rot)
        self.ob= bpy.context.object
        self.ob.name = self.name
        self.ob.data.body = self.name
        self.ob.data.size = 15
        setColor.setMaterial(bpy.context.object, setColor.red) # Elements in white are deformable elements 
        return self.ob