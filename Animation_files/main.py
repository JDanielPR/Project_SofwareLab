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
import mathutils

# Define main function
def main():
    
    imp.reload(myHeader)   #Load library
    myHeader.delete_all()  #Clean everything

    # Define the list of nodes and member
    (nodes,members, numberOfNodes, numberOfMembers, numberOfPaths) = myHeader.leerTxt()   
    my_nodes = []     #Define nodes list
    my_elements = []  #Define memberslist
    
    # Definition of variables
    cursor = context.scene.cursor_location            #Set the cursor location
    start_pos = (0,0,0)                               #Define the first position
    generalMemberList = []                            #Contains all members of the structure
    coordinatesInX = []                               #List of all coordinates in x
    totalPathLength = []                              #List of the lengths per path
    coverableLengthPerPath = []                       #List of the maximum length that a load path can deform
    finalPathLength = []                              #List of the maximum length that a load path can reach
    horizontalMemberListPerPath = []                  #List of objects Members that are in horizontal position
    inclinedMemberListPerPath = []                    #List of objects Memebers that are in inclined position
    DistancesFromTheFistNodeToTheHeadOfEachPath = []
    coordinateOfTheVeryFirstNode = 0
    finalLengthOfTheLongestPath = 0
    
    # Create all node objects
    for i in range(numberOfNodes):  
        # Node(numberOfNode, X, Y ,Z) 
        my_nodes.append(myHeader.Node(i+1, nodes[i][0],nodes[i][1],nodes[i][2], nodes[i][3]))
        coordinatesInX.append(nodes[i][0])
    coordinateOfTheVeryFirstNode = min(coordinatesInX)
    
    # Create all member objects
    for i in range(numberOfMembers-1):
        # Element(numberOfmember, nodeA, nodeB ,startingLoadpath , finalLoadpath, elementType, deformation, velocity, time1, time2,orderOfDeformation)
        my_elements.append(myHeader.Element( i+1 ,my_nodes[int(members[i][0])-1],my_nodes[int(members[i][1])-1],members[i][2],members[i][3],members[i][4],members[i][5],members[i][6],members[i][7],members[i][8],members[i][9]))     

    # Clasify member according to the path
    l = 0
    k = 0
    for i in range(numberOfPaths+1):
        horizontalMemberListPerPath.append([])
        for j in range(len(my_elements)):
            if my_elements[j].get_startingLoadpath() == my_elements[j].get_finalLoadpath():
                if my_elements[j].get_startingLoadpath() == i + 1:
                    horizontalMemberListPerPath[i].append(my_elements[j])
                    # Define length per path
                    l = my_elements[j].calcLength() + l
                    if my_elements[j].get_elementType() == 0 or my_elements[j].get_elementType() == 2:
                        k = my_elements[j].calcLength() + k
        totalPathLength.append(l)
        coverableLengthPerPath.append(k)
        l = 0
        k = 0
    
    # Define a list with the final length of each path
    for i in range(numberOfPaths + 1):
        finalPathLength.append(totalPathLength[i] - coverableLengthPerPath[i])
    
    finalLengthOfTheLongestPath = max(finalPathLength)
    print(finalPathLength)
    print(finalLengthOfTheLongestPath)
    
    # Define the list of inclined members per Path
    for j in range(len(my_elements)):
            if my_elements[j].get_startingLoadpath() != my_elements[j].get_finalLoadpath():
                inclinedMemberListPerPath.append(my_elements[j])
                
    # Create wall
    bpy.ops.mesh.primitive_cube_add(location = (coordinateOfTheVeryFirstNode - 1000,0,0), rotation=(0,0,math.radians(90)))
    bpy.context.object.dimensions = 3000, 1000, 100
    bpy.ops.object.shade_smooth() 
    w = bpy.context.object
    w.name = "Wall"

    # Select wall
    bpy.context.scene.objects.active = bpy.data.objects["Wall"]
    bpy.data.objects['Wall'].select = True  
    bpy.ops.object.select_all(action = 'TOGGLE')
    
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = 30
    ####################################################################
    # Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
    for i in range(len(my_elements)):
        cube = my_elements[i].get_member()
        cube.keyframe_insert('location', frame=1)
        cube.keyframe_insert('location', frame=10)     
    #print(my_elements[9].get_member().location[0] )
    #Move all the elements at the initial position  
    for i in range(len(my_elements)):
        cube = my_elements[i].get_member()
        bpy.context.scene.frame_current = 30
        cube.location[0] -= 500
        cube.keyframe_insert('location', frame = 30)
        fcurves = cube.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR' 
    #################################################################### 
    #print(my_elements[9].get_member().location[0] )
    '''
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
    #print(tiempos)
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
    scn.frame_end = 120
    
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
    '''
'''
######################################################################################
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()
bpy.ops.object.select_by_type(type='LAMP')
bpy.ops.object.delete()
bpy.ops.object.select_by_type(type='CAMERA')
bpy.ops.object.delete()
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
'''


#Delete everything
myHeader.initialize()
#Call the main function
main()
#Start animation
#bpy.ops.screen.animation_play(reverse=False, sync=False) 
# draw node
# draw node
