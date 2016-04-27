'''
Created on 25/03/2016

@author: Admin
'''
import bpy   #Module for blender
import math
import myHeader
import colores
import imp
import random
from bpy import context
from mathutils import Vector

#Define variables for primitive shapes
cubeobject = bpy.ops.mesh.primitive_cube_add
sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
cylinderobject = bpy.ops.mesh.primitive_cylinder_add

#Define the main function
def main():
    delete_all()         #Clean everything
    imp.reload(colores)  #Carga librerias
    imp.reload(myHeader) #Carga librerias
    
    
    
    red = makeMaterial('Red', (1,0,0), (1,1,1), 1)
    blue = makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
    
    #Wall
    bpy.ops.mesh.primitive_cube_add(location = (-100,0,0), rotation=(0,0,math.radians(90)))
    w = bpy.context.object
    w.name = "Wall"
    bpy.ops.transform.resize(value = (100,400, 20)) #for cube
    bpy.ops.object.shade_smooth() 
    setMaterial(bpy.context.object, blue)
    
    (nodes,tubes, numberNodes, numberTubes) = myHeader.leerTxt()
    my_nodes = []  #Define lista de nodos
    my_tubes = []  #Define lista de tubos
    for i in range(numberNodes):
        my_nodes.append(myHeader.Node(i+1, nodes[i][0],nodes[i][1],nodes[i][2]))
    for i in range(numberTubes):
        my_tubes.append(myHeader.Tube(i+1,my_nodes[int(tubes[i][0])-1],my_nodes[int(tubes[i][1])-1],tubes[i][2],tubes[i][3],tubes[i][4]))
        
    #Define variables
    cursor = context.scene.cursor_location  #Set the cursor location
    start_pos = (0,0,0)  #Define the first position

    x = 0.0
    y = 0.0
    z = 0.0
    c = 0.0
    
    cubeSet = []

    # Create red cube
    setMaterial(bpy.context.object, red)

    for i in range(numberTubes):
        inx1 = my_tubes[i].get_A() - 1
        iny1 = my_tubes[i].get_A() - 1
        inx2 = my_tubes[i].get_B() - 1
        iny2 = my_tubes[i].get_B() - 1
        
        xi = (my_nodes[inx1].get_x()) 
        yi = (my_nodes[iny1].get_y()) 
        xj = (my_nodes[inx2].get_x()) 
        yj = (my_nodes[iny2].get_y()) 
        
        a1 = 0
        a2 = math.radians(90)
        a3 = 0
        
        x = xi
        y = yi
        z = 0.0
        createElementCube(str(i), (x, y, z),my_tubes[i].get_d(), my_tubes[i].calcLength(),(a1, a2, a3))
        selectedObject = bpy.context.selected_objects
        mesh = selectedObject[0]
        cubeSet.append(selectedObject[0])
        c += 50 #color
        
        if my_tubes[i].get_up() == 0:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(255.0, c+ 2 ,23.0)
            bpy.ops.object.shade_smooth() 
        else:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(255.0, 255.0, 255.0)
            bpy.ops.object.shade_smooth() 
 
    bpy.context.scene.objects.active = bpy.data.objects["Wall"]
    bpy.data.objects['Wall'].select = True  
    bpy.ops.object.select_all(action = 'TOGGLE')
    
        
    # get the current scene
    scn = bpy.context.scene

    # assign new duration value
    scn.frame_start = 0
    scn.frame_end = 150
    # 004 Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for cube in cubeSet:
        cube.keyframe_insert('location', frame=1)
        cube.keyframe_insert('location', frame=10)  
        
    
    for cube in cubeSet:
        bpy.context.scene.frame_current = 30
        cube.location[0] -= 50
        cube.keyframe_insert('location', frame=30)
        
    #Path 2                 
    # 005 A Move our Cubes to new position (5 unit in positive Y) at frame 20 and set keyframes
    i = 1
    orden =  [[] for i in range(4)]
    path2 = []
    while i <5:
        j = int(my_tubes[i].get_nt())
        k = int(my_tubes[i].get_num())
        orden[i-1] = [j,k-1]
        i += 1  
    print(orden)
    sort(orden , 4)
    i = 0

    print(orden)
    i = 1
    time = 0
    while i <= 4:
        k = orden[i-1][1]
        print (k)
        cube = cubeSet[k]
        bpy.context.scene.frame_current = 30 + time  
        cube.keyframe_insert('scale', frame=30 + time)
        bpy.context.scene.frame_current = 60 + time
        cube.keyframe_insert('location', frame=60 + time)
        cube.scale[2] *= 0.0
        cube.keyframe_insert('scale', frame=60 +time)
    
        cube = cubeSet[k]
        bpy.context.scene.frame_current = 30 + time
        cube.keyframe_insert('location', frame=32.5 + time)
        bpy.context.scene.frame_current = 60 + time
        cube.location[0] = 0 
        cube.keyframe_insert('location', frame=60 + time)
    
        count = k+1
        offset = 0
        while count <= 4:
            cube = cubeSet[count]
            bpy.context.scene.frame_current = 29.5+ time
            cube.keyframe_insert('location', frame=29.5+ time)
            bpy.context.scene.frame_current = 60+ time
            cube.location[0] = my_tubes[count].calcLength()/2 + offset
            offset =  my_tubes[count].calcLength() + offset
            cube.keyframe_insert('location', frame=60 + time)
            count += 1
            
        i += 1
        time +=30

###########################################################################
#Orden con algoritmo de burburja
def sort(arry, n):
    var1 = 0
    k = 0
    while k < n:
        j = n-2
        while  j >= k:
            if (arry[j] > arry[j+1]):
                var1 = arry[j+1]
                arry[j + 1] = arry[j]
                arry[j] = var1
            j -= 1
        k+= 1
             

def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
    
def createElementCube(name, loc, r ,d, rot):
    cubeobject (
                       location = loc,
                       rotation=rot )                 
    bpy.ops.transform.resize(value = (d*0.5,10, 20)) #for cube
    bpy.ops.transform.translate(value=(d/2,0,0)) #Tranlacion
    ob = bpy.context.object
    ob.name = "E" + name 
    return ob

def createElementNode(name, loc):
    sphereobject (
                       location = loc,
                       size = 1.2)                 
    ob = bpy.context.object
    ob.name = "N" + name 
    return ob

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
######################################################################################
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

#Call the main function
main()



