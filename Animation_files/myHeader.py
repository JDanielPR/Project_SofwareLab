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
        
def leerTxt():
    print ("Herzlich willkommen")
    file = open("C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\Animation_files\Example5.txt", "r") 
    
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
    for i in range(0 , numberNodes + numberTubes):
        if i < numberNodes:
            nodes.append([])
            for j in range(8*(i+1)-8,8*(i+1)):
                nodes[i].append(float(arreglo[j]))
        else:
            tubes.append([])
            for j in range(8*(i+1)-8,8*(i+1)):
                tubes[i - numberNodes].append(float(arreglo[j]))

    return (nodes, tubes , numberNodes, numberTubes,numberPaths)

class Node():
    def __init__(self , num = 0 , cx = 0.0 , cy = 0.0 , cz = 0.0):
        self.num = num
        self.cx = cx
        self.cy = cy
        self.cz = cz
        
    def get_num(self):
        return self.num
    def get_x(self):
        return self.cx
    def get_y(self):
        return self.cy
    def get_z(self):
        return self.cz
        
class Element():
    def __init__(self , num  , nodeA , nodeB  , startingLoadpath , deformation, numberOfElementInLoadpath, elementType, time1, time2):
        self.num = num
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.startingLoadpath = startingLoadpath
        self.deformation = deformation
        self.numberOfElementInLoadpath = numberOfElementInLoadpath
        self.elementType = elementType
        self.time1 = time1
        self.time2 = time2
        
    def get_num(self):
        return self.num
    def get_A(self):
        return self.nodeA.get_num()
    def get_B(self):
        return self.nodeB.get_num()
    def get_startingLoadpath (self):
        return self.startingLoadpath 
    def get_deformation(self):
        return self.deformation
    def get_numberOfElementInLoadpath(self):
        return self.numberOfElementInLoadpath
    def get_elementType(self):
        return self.elementType
    def calcLength(self):
        return math.sqrt((self.nodeA.get_x() - self.nodeB.get_x()) ** 2 + (self.nodeA.get_y() - self.nodeB.get_y()) ** 2)
    def get_time1(self):
        return self.time1
    def get_time2(self):
        return self.time2
   
###########################################################################
#Orden con algoritmo de burburja
def sort(arry, n):
    var1 = 0
    k = 0
    while k < n:
        j = n - 2
        while  j >= k:
            if (arry[j] > arry[j+1]):
                var1 = arry[j+1]
                arry[j + 1] = arry[j]
                arry[j] = var1
            j -= 1
        k+= 1
        
def sortPath(arry, n):
    var1 = 0
    k = 0
    while k < n:
        j = n - 2
        while  j >= k:
            if (arry[j][2] > arry[j+1][2]):
                var1 = arry[j+1]
                arry[j + 1] = arry[j]
                arry[j] = var1
            j -= 1
        k+= 1
             
def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
    
def createElementCube(name, loc, d, rot):
    cubeobject (
                       location = loc,
                       rotation=rot ) 
    bpy.context.object.dimensions = 100, 100, d          
    ob = bpy.context.object
    ob.name = "M" + name 
    return ob

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

    
