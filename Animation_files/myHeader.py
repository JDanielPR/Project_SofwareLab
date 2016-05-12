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

imp.reload(colores)    #Load library
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

    for i in range(0 , numberNodes + numberTubes-1):
        if i < numberNodes:
            nodes.append([])
            for j in range(4*(i+1)-4,4*(i+1)):
                nodes[i].append(float(arreglo[j])) 
            k =  4*(i+1)
            
        else:
            tubes.append([])
            for j in range(k, k + 10):
                tubes[i - numberNodes].append(float(arreglo[j]))
            k = k + 10   
            
    return (nodes, tubes , numberNodes, numberTubes,numberPaths)
#######################################################################################################
class Node():
    def __init__(self , num = 0 , cx = 0.0 , cy = 0.0 , cz = 0.0, nodeType = 0.0):
        self.num = num
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.nodeType  = nodeType   
    def get_num(self):
        return self.num
    def get_x(self):
        return self.cx
    def get_y(self):
        return self.cy
    def get_z(self):
        return self.cz
    def get_nodeType (self):
        return self.nodeType 
#########################################################################################################        
class Element():
    def __init__(self , num  , nodeA , nodeB  , startingLoadpath , finalLoadpath, elementType, deformation, velocity, time1, time2,orderOfDeformation):
        self.num = num
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.startingLoadpath = startingLoadpath
        self.finalLoadpath = finalLoadpath
        self.elementType = elementType
        self.deformation = deformation
        self.velocity = velocity
        self.time1 = time1
        self.time2 = time2
        self.orderOfDeformation = orderOfDeformation 
        self.member= []
        
        # Define coordinates of a member 
        xi = self.nodeA.get_x()
        yi = self.nodeA.get_y() 
        xj = self.nodeB.get_x()
        yj = self.nodeB.get_y()
        # Define inclination of a member
        a1 = 0
        a2 = math.radians(90)
        a3 = math.atan2(yj - yi , xj - xi)
        # Define angle of a member on the working plane
        x = xj - (xj - xi) / 2
        y = yj - (yj - yi) / 2
        z = 0.0
        # Create element
        if self.elementType != 2:
            self.member = createMember(str(self.num), (x, y, z), self.calcLength(),(a1, a2, a3),self.get_elementType())
            selectedObject = bpy.context.selected_objects
            # Clasify two list, one for rigid elements and the other for deformable elements
            if self.get_elementType() == 1:   
                colores.setMaterial(bpy.context.object, black)
            else:  
                colores.setMaterial(bpy.context.object, white)   
            bpy.ops.object.shade_smooth() 
        else:
            self.member = createGap(str(self.num), (x, y, z), self.calcLength(),(a1, a2, a3),self.get_elementType())
        
    def get_num(self):
        return self.num
    def get_A(self):
        return self.nodeA.get_num()
    def get_B(self):
        return self.nodeB.get_num()
    def get_startingLoadpath (self):
        return self.startingLoadpath
    def get_finalLoadpath (self):
        return self.finalLoadpath 
    def get_elementType(self):
        return self.elementType
    def get_deformation(self):
        return self.deformation
    def get_time1(self):
        return self.time1
    def get_time2(self):
        return self.time2
    def get_numberOfElementInLoadpath(self):
        return self.numberOfElementInLoadpath
    def get_member(self):
        return self.member
    def calcLength(self):
        return math.sqrt((self.nodeA.get_x() - self.nodeB.get_x()) ** 2 + (self.nodeA.get_y() - self.nodeB.get_y()) ** 2)   
######################################################################################
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

    
