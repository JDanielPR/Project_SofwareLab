import bpy   #Module for blender
import math
import imp
import random
from bpy import context
import colores

imp.reload(colores)    #Load library

#Define colors
red = colores.makeMaterial('Red', (1,0,0), (1,1,1), 1)
blue = colores.makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
black = colores.makeMaterial('Black', (0,0,0), (2.5,1.5,1), 0.5) 
white = colores.makeMaterial('White', (1,1,1), (2.5,1.5,1), 0.5) 

def initialize():
    # gather list of items of interest.
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    # select them only.
    for object_name in candidate_list:
        bpy.data.objects[object_name].select = True  

    # remove all selected.
    bpy.ops.object.delete()

    bpy.ops.object.select_by_type(type = 'MESH')
    bpy.ops.object.delete(use_global=False)
    for item in bpy.data.meshes:
        item.user_clear() # make it have zero users 
        bpy.data.meshes.remove(item)
   
def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
    


    
