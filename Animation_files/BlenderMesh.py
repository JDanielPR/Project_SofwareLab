import bpy   #Module for blender
import math
import setColor
import imp
from bpy import context

from abc import ABCMeta, abstractmethod

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
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = 50, 50, self.length          
        ob = bpy.context.object
        if self.type == 0:  
            ob.name = "D" + self.name
            #ob.show_name = True
        elif self.type == 1:
            ob.name = "ND" + self.name
            #ob.show_name = True
        return ob

class BlenderGap(BlenderMesh):
    def __init__(self , name, loc, length, rot):
        self.name = name
        self.loc  = loc
        self.length = length
        self.rot = rot
        
    def get_geometricalObject(self):
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = 0, 0, self.length          
        ob = bpy.context.object
        ob.name = "Gap" + self.name 
        return ob
    
class BlenderWall(BlenderMesh):
    def __init__(self , name, loc, height, rot):
        self.name = name
        self.loc  = loc
        self.height = height
        self.rot = rot
        
    def get_geometricalObject(self):
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = self.height + self.height/3, 1000, 100        
        ob = bpy.context.object
        ob.name = "Wall" + self.name 
        return ob
    
class BlenderNode(BlenderMesh):
    def __init__(self , name, loc, rot):
        self.name = name
        self.loc  = loc
        self.rot = rot
        
    def get_geometricalObject(self):
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = 50, 50, 50          
        ob = bpy.context.object
        ob.name = "N" + self.name 
        return ob
    
class BlenderMass(BlenderMesh):
    def __init__(self , name, loc):
        self.name = name
        self.loc  = loc
        self.diameter = 1.2
        
    def get_geometricalObject(self):
        sphereobject (
                       location = self.loc,
                       size = self.diameter)                 
        ob = bpy.context.object
        ob.name = name 
        ob.show_name = True
        return ob
    
class BlenderText(BlenderMesh):
    def __init__(self , name, loc, rot):
        self.name = name
        self.loc = loc
        self.rot =rot
    
    def get_geometricalObject(self):
        bpy.ops.object.text_add( location = self.loc, rotation = self.rot)
        ob= bpy.context.object
        ob.name = "e" + self.name 
        #self.ob.name = self.name
        ob.data.body = self.name
        ob.data.size = 70
        setColor.setMaterial(bpy.context.object, setColor.red) # Elements in white are deformable elements 
        return ob




