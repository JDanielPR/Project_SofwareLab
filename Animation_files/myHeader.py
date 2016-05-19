'''
Created on 06/04/2016

@author: Admin
'''
import bpy   #Module for blender
import math
import imp
import random
from bpy import context
from mathutils import Vector
import colores
import Node

imp.reload(colores)    #Load library
imp.reload(Node)    #Load library
#Define colors
red = colores.makeMaterial('Red', (1,0,0), (1,1,1), 1)
blue = colores.makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
black = colores.makeMaterial('Black', (0,0,0), (2.5,1.5,1), 0.5) 
white = colores.makeMaterial('White', (1,1,1), (2.5,1.5,1), 0.5) 
#Define variables for primitive shapes
cubeobject = bpy.ops.mesh.primitive_cube_add
sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
cylinderobject = bpy.ops.mesh.primitive_cylinder_add

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
########################################################################################################        
def leerTxt():
    file = open("C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\Animation_files\Example8.txt", "r") 
    
    numberNodes = 0
    numberTubes = 0
    numberPaths = 0
    numberNodes = int(file.readline())
    numberTubes = int(file.readline())
    numberPaths = int(file.readline())
    arreglo = []
    nodes = []
    tubes = []
    
    arreglo = file.read().split()
    file.close()
    k = 0

    for i in range(numberNodes + numberTubes ):
        if i < numberNodes:
            nodes.append([])
            for j in range(3*(i+1)-3,3*(i+1)):
                nodes[i].append(float(arreglo[j])) 
            k =  3*(i+1)
            
        else:
            tubes.append([])
            for j in range(k, k + 7):
                tubes[i - numberNodes].append(float(arreglo[j]))
            k = k + 7   
            
    return (nodes, tubes , numberNodes, numberTubes,numberPaths)
#######################################################################################################
def createMember(name, loc, d, rot,type):
    cubeobject (
                       location = loc,
                       rotation=rot ) 
    bpy.context.object.dimensions = 50, 50, d          
    ob = bpy.context.object
    if type == 0:
        ob.name = "Deformable_part" + name 
    elif type == 1:
        ob.name = "Rigid_part" + name 
    return ob

def createGap(name, loc, d, rot,type):
    cubeobject (
                       location = loc,
                       rotation=rot ) 
    bpy.context.object.dimensions = 0, 0, d          
    ob = bpy.context.object
    ob.name = "gap" + name 
    return ob
######################################################################################       
def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
    
def createElementNode(name, loc, d):
    sphereobject (
                       location = loc,
                       size = d)                 
    ob = bpy.context.object
    ob.name = "N" + name 
    return ob

def createConection(name, loc, l, d, rot):
    cubeobject (
                       location = loc,
                       rotation=rot ) 
    bpy.context.object.dimensions = 100, l , d          
    ob = bpy.context.object
    ob.name = "C" + name 
    return ob

    
