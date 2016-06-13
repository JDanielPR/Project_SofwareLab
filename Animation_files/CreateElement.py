import bpy   #Module for blender
import math
import imp
import random
from bpy import context
from mathutils import Vector
import colores
import Node
import bpy
from abc import ABCMeta, abstractmethod

#Define variables for primitive shapes
cubeobject = bpy.ops.mesh.primitive_cube_add
sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
cylinderobject = bpy.ops.mesh.primitive_cylinder_add

class CreateElement:
    __metaclass__ = ABCMeta

    @abstractmethod
    def geometricalObject(self): pass

class CreateMemberInAnimation(CreateElement):
    def __init__(self , name, loc, length, rot,type):
        self.name = name
        self.loc  = loc
        self.length = length
        self.rot = rot
        self.type = type
        
    def geometricalObject(self):
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

class CreateGapInAnimation(CreateElement):
    def __init__(self , name, loc, length, rot):
        self.name = name
        self.loc  = loc
        self.length = length
        self.rot = rot
        
    def geometricalObject(self):
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = 0, 0, self.length          
        ob = bpy.context.object
        ob.name = "Gap" + self.name 
        return ob
    
class CreateNodeInAnimation(CreateElement):
    def __init__(self , name, loc, rot):
        self.name = name
        self.loc  = loc
        self.rot = rot
        
    def geometricalObject(self):
        cubeobject (
                       location = self.loc,
                       rotation = self.rot ) 
        bpy.context.object.dimensions = 100, 100, 100          
        ob = bpy.context.object
        ob.name = "N" + self.name 
        return ob
    
class CreateMassInAnimation(CreateElement):
    def __init__(self , name, loc):
        self.name = name
        self.loc  = loc
        self.diameter = 1.2
        
    def geometricalObject(self):
        sphereobject (
                       location = self.loc,
                       size = self.diameter)                 
        ob = bpy.context.object
        ob.name = name 
        ob.show_name = True
        return ob




