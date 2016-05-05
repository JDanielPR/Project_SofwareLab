'''
Created on 25/03/2016

@author: Admin
'''
import bpy   #Module for blender
import math
import imp
import random
from bpy import context
from mathutils import Vector
from math import pi

import myHeader
import colores
import draw_member

#Define the main function
def main():
    
    imp.reload(colores)  #Carga librerias
    imp.reload(myHeader) #Carga librerias
    myHeader.delete_all()         #Clean everything

    red = colores.makeMaterial('Red', (1,0,0), (1,1,1), 1)
    blue = colores.makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
    gray= colores.makeMaterial('BlueSemi', (1,1,1), (2.5,1.5,1), 0.5)
    
    #Wall
    bpy.ops.mesh.primitive_cube_add(location = (-500,0,0), rotation=(0,0,math.radians(90)))
    w = bpy.context.object
    w.name = "Wall"
    bpy.ops.transform.resize(value = (500,2000, 20)) #for cube
    bpy.ops.object.shade_smooth() 
    colores.setMaterial(bpy.context.object, gray)
    
    (nodes,tubes, numberOfNodes, numberOfMembers, numberOfPaths) = myHeader.leerTxt()   
    my_nodes = []  #Define nodes list
    my_elements = []  #Define elements list
    
    for i in range(numberOfNodes):
        my_nodes.append(myHeader.Node(i+1, nodes[i][0],nodes[i][1],nodes[i][2]))
    for i in range(numberOfMembers):
        my_elements.append(myHeader.Element( i+1 ,my_nodes[int(tubes[i][0])-1],my_nodes[int(tubes[i][1])-1],tubes[i][2],tubes[i][3],tubes[i][4],tubes[i][5],tubes[i][6],tubes[i][7]))

    #Define variables
    cursor = context.scene.cursor_location  #Set the cursor location
    start_pos = (0,0,0)  #Define the first position

    x = 0.0
    y = 0.0
    z = 0.0
    c = 0.0
    
    cubeSet = []
    sphereSet = []
    nodesSet = []
    tiempos = []
    scales = []

    for i in range(numberOfMembers):
        inx1 = my_elements[i].get_A() - 1
        iny1 = my_elements[i].get_A() - 1
        inx2 = my_elements[i].get_B() - 1
        iny2 = my_elements[i].get_B() - 1
        
        xi = (my_nodes[inx1].get_x()) 
        yi = (my_nodes[iny1].get_y()) 
        xj = (my_nodes[inx2].get_x()) 
        yj = (my_nodes[iny2].get_y()) 
        #Define angles
        a1 = 0
        a2 = math.radians(90)
        a3 = 0
        # Define coordinates
        x = xi + (xj - xi) / 2
        y = yi
        z = 0.0
        
        #if my_elements[i].get_time1() != 0:
        t1 = my_elements[i].get_time1()
        t2 = my_elements[i].get_time2()
        tiempos.append([t1, t2])
        
        es = my_elements[i].get_deformation()
        scales.append(es)

        if my_elements[i].get_elementType() == 1:
            sphereSet.append(myHeader.createElementNode(str(i), (x, y, -100),50))
            bpy.ops.object.shade_smooth() 
            colores.setMaterial(bpy.context.object, red)
        else:
            sphereSet.append(myHeader.createElementNode(str(i), (x, y, -100),0))
            bpy.ops.object.shade_smooth() 
            colores.setMaterial(bpy.context.object, red)
      
        myHeader.createElementCube(str(i), (x, y, z), my_elements[i].calcLength(),(a1, a2, a3))
        selectedObject = bpy.context.selected_objects
        mesh = selectedObject[0]
        cubeSet.append(selectedObject[0])
        
        if my_elements[i].get_elementType() == 0:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(0.0, 0.0, 0.0)
            bpy.ops.object.shade_smooth() 
            
            nodesSet.append(myHeader.createConection(str(i), (xj, yj, -100), 0, 0, (0, math.radians(90), 0)))
            bpy.ops.object.shade_smooth() 
            colores.setMaterial(bpy.context.object, gray)
            
        else:
            getactiveobject = bpy.context.selected_objects[0]
            getactiveobject.active_material = colores.initcolors(255.0, 255.0, 255.0)
            bpy.ops.object.shade_smooth() 
            
            nodesSet.append(myHeader.createConection(str(i), (xi, yi, -100), 150, 20, (0, math.radians(90), 0)))
            bpy.ops.object.shade_smooth() 
            colores.setMaterial(bpy.context.object, gray)
 
        
    #print(scales)   
    # create background
    '''
    bpy.ops.mesh.primitive_plane_add(location=(1000,0,-4))  
    plane = bpy.context.object  
    plane.dimensions = (3000,3000,0)
    bpy.ops.object.shade_smooth() 
    colores.setMaterial(bpy.context.object, blue)'''

    ####################################################################
    bpy.context.scene.objects.active = bpy.data.objects["Wall"]
    bpy.data.objects['Wall'].select = True  
    bpy.ops.object.select_all(action = 'TOGGLE')
    ####################################################################
    #Path                
    # Clasify our elements 
    i = 0
    time = 0
    numberOfDeformableElementsPerPath = 0
    numberOfElementsPerPath = 0
    deformableElements = list()
    rigidElements = list()
    coordinatesX = list()
    totalElements = list()
    arraynumberOfDeformableElementsPerPath  = list()
    arraynumberOfElementsPerPath  = list()
    path = []
    
    for i in range(numberOfMembers):
        pathNumber = int(my_elements[i].get_startingLoadpath())
        positionInPath = int(my_elements[i].get_numberOfElementInLoadpath())
        numberOfElement = int(my_elements[i].get_num())
        totalElements.append([ positionInPath, numberOfElement - 1, pathNumber])

    for i in range(numberOfMembers):
        pathNumber = int(my_elements[i].get_startingLoadpath())
        positionInPath = int(my_elements[i].get_numberOfElementInLoadpath())
        numberOfElement = int(my_elements[i].get_num())
        
        if positionInPath != 0:
            deformableElements.append([ positionInPath, numberOfElement - 1, pathNumber])
        else:
            rigidElements.append([positionInPath, numberOfElement - 1, pathNumber ])
    
    myHeader.sort(deformableElements, len(deformableElements))
    myHeader.sortPath(deformableElements, len(deformableElements)) 
    
    h = numberOfPaths
    count = 0
    for i in range(numberOfPaths):
        for j in range(len(deformableElements)):
            if deformableElements[j][2] == h:
                count += 1
                numberOfDeformableElementsPerPath = count
            
        arraynumberOfDeformableElementsPerPath.append([count])
        count = 0
        h -= 1
       
    #print(totalElements)    
    h = numberOfPaths
    count = 0
    for i in range(numberOfPaths):
        for j in range(len(totalElements)):
            if totalElements[j][2] == h:
                count += 1
                numberOfElementsPerPath = count
            
        arraynumberOfElementsPerPath.append([count])
        count = 0
        h -= 1
        
    #print(deformableElements)
    #print(arraynumberOfDeformableElementsPerPath)
    #print(arraynumberOfElementsPerPath)    
    # Find the element which is the closest to the wall
    for i in range(numberOfNodes):
        coordinatesX.append((nodes[i][0]))
    
    initialStep = min(coordinatesX)   
             
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = 90
    
    # Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for cube in cubeSet:
        cube.keyframe_insert('location', frame=1)
        cube.keyframe_insert('location', frame=10)  
    
    #Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for sphere in sphereSet:
        sphere.keyframe_insert('location', frame=1)
        sphere.keyframe_insert('location', frame=10) 
       
    #Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for conections in nodesSet:
        conections.keyframe_insert('location', frame=1)
        conections.keyframe_insert('location', frame=10) 
      
    #Move all the elements at the initial position  
    for cube in cubeSet:
        bpy.context.scene.frame_current = 30
        cube.location[0] -= initialStep
        cube.keyframe_insert('location', frame = 30)
        fcurves = cube.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'  
                   
    #Move all masses at the initial position  
    for sphere in sphereSet:
        bpy.context.scene.frame_current = 30
        sphere.location[0] -= initialStep
        sphere.keyframe_insert('location', frame = 30)
        fcurves = sphere.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'  
                
    #Move all the nodes at the initial position  
    for conections in nodesSet:
        bpy.context.scene.frame_current = 30
        conections.location[0] -= initialStep
        conections.keyframe_insert('location', frame = 30)
        fcurves = conections.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'  
                    
    offset  = 0
    offset1 = 0
    offset2 = 0
    print(arraynumberOfDeformableElementsPerPath)
    print(arraynumberOfElementsPerPath)
    print(deformableElements)

    #P a t h
    for g in range(numberOfPaths):
        numberOfDeformableElements = arraynumberOfDeformableElementsPerPath[numberOfPaths-g-1][0]
        numberOfElementsInPath = arraynumberOfElementsPerPath[numberOfPaths-g-1][0]
        
        #print(numberOfDeformableElements)
        #print(numberOfElementsInPath )
        
        for i in range(numberOfDeformableElements):  
            k = deformableElements[i + offset][1]
            cube = cubeSet[k]
            sphere = sphereSet[k]
            conections = nodesSet[k]
            pos  = cube.location[0]
            print(k)
        
            # Translate the element
            bpy.context.scene.frame_current = tiempos[k][0]#(30  + time)
            cube.keyframe_insert('location', frame=tiempos[k][0])#(30 + time))
            bpy.context.scene.frame_current = tiempos[k][1]#(60 + time)
            cube.location[0] =  pos - (1-scales[k])* my_elements[k].calcLength()/2
            cube.keyframe_insert('location', frame = tiempos[k][1])#(60  + time))
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                   
            # Translate the element mass
            bpy.context.scene.frame_current = tiempos[k][0]#(30  + time)
            sphere.keyframe_insert('location', frame = tiempos[k][0])#(30 + time))
            bpy.context.scene.frame_current = tiempos[k][1]#(60 + time)
            sphere.location[0] = pos - (1-scales[k])*my_elements[k].calcLength()/2
            sphere.keyframe_insert('location', frame = tiempos[k][1])#(60 + time))
            fcurves = sphere.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
            
            # Translate the element nodes
            bpy.context.scene.frame_current = tiempos[k][0]#(30  + time)
            conections.keyframe_insert('location', frame = tiempos[k][0])#(30 + time))
            bpy.context.scene.frame_current = tiempos[k][1]#(60 + time)
            conections.location[0] = pos - my_elements[k].calcLength()/2 
            conections.keyframe_insert('location', frame = tiempos[k][1])#(60 + time))
            fcurves = conections.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'     
            
        
            # Deform the element
            bpy.context.scene.frame_current = tiempos[k][0]#(30  + time)
            cube.keyframe_insert('scale', frame = tiempos[k][0])#(30 + time))
            bpy.context.scene.frame_current = tiempos[k][1]#(60 + time)
            cube.scale[2] *= scales[k]
            cube.keyframe_insert('scale', frame= tiempos[k][1])#(60 + time))
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                    
            # Move the rest of the cubes to the wall
            for p in range(numberOfElementsInPath + offset1):
                if p > k:
                    vec  = cubeSet[p].location[0]
                    bpy.context.scene.frame_current = tiempos[k][0]#(30 + time)
                    cubeSet[p].keyframe_insert('location', frame = tiempos[k][0])#(30 + time))
                    sphereSet[p].keyframe_insert('location', frame = tiempos[k][0])#(30 + time))
                    nodesSet[p].keyframe_insert('location', frame = tiempos[k][0])#(30 + time))
                    bpy.context.scene.frame_current = (60 + time)
                    
                    cubeSet[p].location[0] = vec - (1-scales[k])*my_elements[k].calcLength() 
                    cubeSet[p].keyframe_insert('location', frame = tiempos[k][1])#(60 + time)) 
                    sphereSet[p].location[0] = vec - (1-scales[k])* my_elements[k].calcLength() 
                    sphereSet[p].keyframe_insert('location', frame = tiempos[k][1])#(60 + time)) 
                    nodesSet[p].location[0] = vec - (1-scales[k])*my_elements[k].calcLength()- my_elements[p].calcLength()/2 
                    nodesSet[p].keyframe_insert('location', frame = tiempos[k][1])#(60 + time)) 
                    fcurves = cubeSet[p].animation_data.action.fcurves
                    for fcurve in fcurves:
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR'

            time += 30  
        time = 0
        offset = offset + numberOfDeformableElements
        offset1 = offset1 + numberOfElementsInPath 
        
  
######################################################################################

# clear everything for now
scene = bpy.context.scene
scene.camera = None  
for obj in scene.objects:  
    scene.objects.unlink(obj)
####################################################################
lamp_data = bpy.data.lamps.new(name="lampa", type='SUN')  
lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)  
scene.objects.link(lamp_object)  
lamp_object.location = (300, 150, -200)
lamp_object.rotation_euler = (pi,0,0)

# and now set the camera
cam_data = bpy.data.cameras.new(name="cam")  
cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
scene.objects.link(cam_ob)  
cam_ob.location = (576, 170, -1500)  
cam_ob.rotation_euler = (pi,0,0) 
cam_ob.scale = (20, 20, 20)  
cam = bpy.data.cameras[cam_data.name]  
cam.lens = 20
cam.type = 'PERSP'
cam.lens_unit = 'MILLIMETERS'
cam.shift_x = 0.15
cam.shift_y = 0.1
cam.clip_start = 209
cam.clip_end = 900
cam_data.clip_start = 24
cam_data.clip_end = 1500



#Delete everything
myHeader.initialize()
#Call the main function
main()
#Start animation
bpy.ops.screen.animation_play(reverse=False, sync=False) 

 




