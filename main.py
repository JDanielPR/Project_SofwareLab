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

'''#Set the active layers
bpy.context.scene.layers[0] = True
bpy.context.scene.layers[0] = False'''

#Define variables for primitive shapes
cubeobject = bpy.ops.mesh.primitive_cube_add
sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
cylinderobject = bpy.ops.mesh.primitive_cylinder_add
Amt = 0


#Define the main function
def main():
    delete_all()         #Clean everything
    imp.reload(colores)  #Carga librerias
    imp.reload(myHeader) #Carga librerias
    
    (nodes,tubes, numberNodes, numberTubes) = myHeader.leerTxt()
    my_nodes = []  #Define lista de nodos
    my_tubes = []  #Define lista de tubos
    for i in range(numberNodes):
        my_nodes.append(myHeader.Node(i+1, nodes[i][0],nodes[i][1],nodes[i][2]))
    for i in range(numberTubes):
        my_tubes.append(myHeader.Tube(i+1,my_nodes[int(tubes[i][0])-1],my_nodes[int(tubes[i][1])-1],tubes[i][2],tubes[i][3]))
        

    #Define variables
    cursor = context.scene.cursor_location  #Set the cursor location
    start_pos = (0,0,0)  #Define the first position

    x = 0.0
    y = 0.0
    z = 0.0
    
    cubeSet = []

    for i in range(numberTubes):
        #cubeobject(location = (x ,y, z))
        inx1 = my_tubes[i].get_A() - 1
        iny1 = my_tubes[i].get_A() - 1
        inx2 = my_tubes[i].get_B() - 1
        iny2 = my_tubes[i].get_B() - 1
        
        xi = (my_nodes[inx1].get_x()) / 100
        yi = (my_nodes[iny1].get_y()) / 100
        xj = (my_nodes[inx2].get_x()) / 100
        yj = (my_nodes[iny2].get_y()) / 100
        print( xi , " ", xj, "  ", yi , " ", yj)
        a1 = 0
        a2 = math.radians(90)
        a3 = 0
        
        if xi == xj:
            x = xi
        else:
            x = math.fabs(xj - xi)*0.5 + xi
        if yi == yj:
            y = yi
        else:
            y = (yj - yi)*0.5 + yi
        z = 0.0
        
        createElement(str(i), (x, y, z),my_tubes[i].get_d()/2, my_tubes[i].calcLength() / 100,(a1, a2, a3))
        selectedObject = bpy.context.selected_objects
        #bpy.context.object.data.name = "E" + str(i)
        mesh = selectedObject[0]
        cubeSet.append(selectedObject[0])
        
        #y+=10
        #bpy.ops.transform.resize(value = (2 ,20, 2)) #for cube
        #Get the active object and assign it a color
        if my_tubes[i].get_up() == 0:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(255.0, 255.0, 255.0)
        else:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(0.0, 0.0, 0.0)
 
    
    #Wall
    bpy.ops.mesh.primitive_cube_add(location = (-10,0,0), rotation=(0,0,math.radians(90)))
    w = bpy.context.object
    w.name = "Wall"
    bpy.ops.transform.resize(value = (0.2,10, 0.2)) #for cube
    bpy.ops.object.select_all(action = 'TOGGLE')
    #bpy.context.scene.objects.active = bpy.data.objects["E0.012"]
    #bpy.data.objects['E0.012'].select = True  
    #bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR)  
    '''for item in  cubeSet:
        item.select = False'''
        
    # get the current scene
    scn = bpy.context.scene 

    # assign new duration value
    scn.frame_end = 120

    # 004 Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for cube in cubeSet:
        cube.keyframe_insert('location', frame=1)
        cube.keyframe_insert('location', frame=10) 
        
    
    # 005 A Move our Cubes to new position (5 unit in positive Y) at frame 20 and set keyframes

    bpy.context.scene.frame_current = 100  
    
    for cube in cubeSet:
        cube.location[0] -= 10
        cube.keyframe_insert('location', frame=100)
        cube.scale[2] += 0
        cube.keyframe_insert('scale', frame=100)
        
    fra =bpy.context.scene.frame_current
    if fra == 100:
        bpy.context.scene.frame_current = 120 
        for cube in cubeSet:
            cube.location[0] -= 5
            cube.keyframe_insert('location', frame=120)
            cube.scale[2] *= 0.4
            cube.keyframe_insert('scale', frame=120)
            
        
     
    
def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
    
def createElement(name, loc, r ,d, rot):
    cubeobject (
                       location = loc,
                       rotation=rot )
                       
    bpy.ops.transform.resize(value = (d,0.2, 0.2)) #for cube
    bpy.ops.transform.translate(value=loc) #Tranlacion
    #bpy.context.object.data.name = "E" + name
    ob = bpy.context.object
    ob.name = "E" + name 
    #ob.show_name = True
    return ob

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



