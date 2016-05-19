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
from operator import itemgetter # to use max
import myHeader
import colores
import mathutils
import Node
import Element

# Define main function
def main():
    print("The program starts here")
    imp.reload(myHeader)   #Load library
    imp.reload(Node)   #Load library
    imp.reload(Element)   #Load library
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
    coverableLengthPerPath = []                       #List of the maximum length that a load path can deform
    finalPathLength = []                              #List of the maximum length that a load path can reach
    horizontalMemberListPerPath = []                  #List of objects Members that are in horizontal position per path
    horizontalDeformableMemberListPerPath = []        #List of objects Members that are deformablein horizontal position per path
    inclinedMemberListPerPath = []                    #List of objects Memebers that are in inclined position
    distancesFromTheFistNodeToTheHeadOfEachPath = []
    #listOfTheOrderInWhichThePathsWillStartDeforming = []
    finalDeformablePartPerPath = []
    listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming = []
    listOfGapsPerPath = []
    listOfTheNumberOfGapsPerPath = []
    listOfTheDeformablepartReminder = []
    listOfValueOfTheNearestNodeThatBelongsToADeformableMember = []
    listOfTheNumberOfMembersInEachPath = []
    listOfTheNumberOfDeformableMemberAndGaps = []
    listOfTheTimesOfEachPathWillStartDeforming = []
    nonDeformableLengthPerPath = []
    totalPathLength = []                              #List of the lengths per path
    coordinateOfTheVeryFirstNode = 0
    coordinateOfTheVeryLastNode = 0
    finalLengthOfTheLongestPath = 0
    lengthOfTheLongestPath = 0
    pathNumberOfTheLongestFinalPath = 0
    #valueOfTheLengthOfTheLongestDeformableMember = 0
    valueOfTheFurthestNodeThatBelongsToADeformableMember = 0
    valueOfTheNearestNodeThatBelongsToADeformableMember = 0
    timeOfTheAnimation = 0
    #timeOfEachPathToReachTheLengthOfTheLongestNonDeformablePart = []
    
    # Create all node objects
    for i in range(numberOfNodes):  
        # Node(numberOfNode, X, Y ,Z) 
        my_nodes.append(Node.Node(nodes[i][0], nodes[i][1],nodes[i][2]))
        coordinatesInX.append(nodes[i][1])
        
    coordinateOfTheVeryFirstNode = min(coordinatesInX)
    coordinateOfTheVeryLastNode  = max(coordinatesInX)
    # Create all member objects
    for i in range(numberOfMembers):
        # Element(numberOfmember, nodeA, nodeB ,startingLoadpath , finalLoadpath, elementType, deformation,orderOfDeformation)
        my_elements.append(myHeader.Element( i + 1 ,my_nodes[int(members[i][0])-1],my_nodes[int(members[i][1])-1],members[i][2],members[i][3],members[i][4],members[i][5],members[i][6]))     
    
    # Sorting of gaps per path
    countGaps = 0
    for i in range(numberOfPaths):
        listOfGapsPerPath.append([])
        for j in range(len(my_elements)):
            if my_elements[j].get_startingLoadpath() == my_elements[j].get_finalLoadpath():
                if my_elements[j].get_startingLoadpath() == i + 1:
                    if my_elements[j].get_elementType() == 2:
                        countGaps = countGaps + 1
                        listOfGapsPerPath[i].append([my_nodes[int(members[j][0])-1].get_x(), my_elements[j].get_num() ])          
        listOfTheNumberOfGapsPerPath.append(countGaps)
        countGaps = 0  
     
    for i in range(numberOfPaths):
        listOfGapsPerPath[i].sort()
    #print(listOfGapsPerPath)
       
    for i in range(numberOfPaths):
        for j in range(listOfTheNumberOfGapsPerPath[i]):
            #print(listOfGapsPerPath[i][j][1])
            my_elements[listOfGapsPerPath[i][j][1]-1].set_orderOfDeformation(j+1)
            #print(my_elements[listOfGapsPerPath[i][j][1]-1].get_orderOfDeformation())
    
    #print("List of the number of gaps per path")
    #print(listOfTheNumberOfGapsPerPath)
    #print("List of gaps per path")
    #print(listOfGapsPerPath)
      
    # Clasify member according to the path
    l = 0
    k = 0 
    countElements = 0  
    countDeformableElementsAndGaps = 0 
    localNumerationPerPath = 0
    
    for i in range(numberOfPaths):
        horizontalMemberListPerPath.append([])             # Clasify members according to the path
        horizontalDeformableMemberListPerPath.append([])   # Clasify deformable members according to the path
        listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming.append([])
        numberMaxOfGaps = listOfTheNumberOfGapsPerPath[i]
        for j in range(len(my_elements)):
            if my_elements[j].get_startingLoadpath() == my_elements[j].get_finalLoadpath():
                if my_elements[j].get_startingLoadpath() == i + 1:
                    horizontalMemberListPerPath[i].append([my_nodes[int(my_elements[j].get_A() )-1].get_x() , my_elements[j].get_num(), localNumerationPerPath ])
                    countElements = countElements + 1
                    # Define length per path
                    l = my_elements[j].calcLength() + l
                    if my_elements[j].get_elementType() == 0 or my_elements[j].get_elementType() == 2:
                        k = my_elements[j].calcLength()*(my_elements[j].get_deformation()/100)+ k
                        horizontalDeformableMemberListPerPath[i].append(my_elements[j])
                        countDeformableElementsAndGaps = countDeformableElementsAndGaps + 1;
                        if my_elements[j].get_elementType() == 0:
                            listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].append([my_elements[j].get_orderOfDeformation() + numberMaxOfGaps ,my_elements[j].get_num(),my_elements[j].calcLength()*(my_elements[j].get_deformation()/100)/10, my_elements[j].calcLength()*(my_elements[j].get_deformation()/100), my_elements[j].calcLength() ,my_elements[j].get_deformation()])              
                        else:
                            listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].append([my_elements[j].get_orderOfDeformation() , my_elements[j].get_num(),my_elements[j].calcLength()*(my_elements[j].get_deformation()/100)/10, my_elements[j].calcLength()*(my_elements[j].get_deformation()/100), my_elements[j].calcLength() ,my_elements[j].get_deformation()])   
        listOfTheNumberOfDeformableMemberAndGaps.append(countDeformableElementsAndGaps)
        listOfTheNumberOfMembersInEachPath.append(countElements)
        totalPathLength.append(l)          # Total length of the path
        coverableLengthPerPath.append(k)   # Length to cover including gaps
        l = 0
        k = 0
        countElements = 0
        countDeformableElementsAndGaps = 0
        localNumerationPerPath = 0

    # Once knowing the members of each path we proceed to clasify accornding to the position in the path
    for i in range(numberOfPaths):
        horizontalMemberListPerPath[i].sort()

    for i in range(numberOfPaths):
        if len(horizontalMemberListPerPath[i]) > 0:
            listOfValueOfTheNearestNodeThatBelongsToADeformableMember.append(horizontalMemberListPerPath[i][0]) 
    
    valueOfTheFurthestNodeThatBelongsToADeformableMember = max(max(horizontalMemberListPerPath))[0] 
    valueOfTheNearestNodeThatBelongsToADeformableMember = (min(listOfValueOfTheNearestNodeThatBelongsToADeformableMember))[0] 
      
    # Enumarate the member of a path locally
    n = 1
    for i in range(numberOfPaths):
        for j in range(listOfTheNumberOfMembersInEachPath[i]):
            horizontalMemberListPerPath[i][j][2] = n
            n =  n + 1
        n = 1 
    print("First node")
    print(coordinateOfTheVeryFirstNode)
    print("Last node")
    print(coordinateOfTheVeryLastNode)   
    print("Number of elements per path")
    print(listOfTheNumberOfMembersInEachPath)
    print("List of the horizontal elements per path")
    print(horizontalMemberListPerPath)
    #print("Number of deformable elements and gaps per path")
    #print(listOfTheNumberOfDeformableMemberAndGaps)
    #print("Value of the furthest node that belongs to a deformable member")
    #print(valueOfTheFurthestNodeThatBelongsToADeformableMember)
    #print("Value of the nearest node that belongs to a deformable member")
    #print(valueOfTheNearestNodeThatBelongsToADeformableMember)
    #print("Sequence per path: ") 
    #print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)
    
    # Once knowing the member of each path we proceed to clasify accornding to the OoD
    for i in range(numberOfPaths):
        #sorted(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i],key=lambda x: (x[0]))
        listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].sort()
        
    #print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)

    ####################################################################################
    # Define a list with the length of the non deformable part
    for i in range(numberOfPaths):
        nonDeformableLengthPerPath.append(totalPathLength[i] - coverableLengthPerPath[i])
    
    finalLengthOfTheLongestPath = max(nonDeformableLengthPerPath )  #Final length of the complete system in
    #valueOfTheLengthOfTheLongestDeformableMember = max(coverableLengthPerPath)
    lengthOfTheLongestPath = max(totalPathLength)
    
    print("Total path length : ") 
    print(totalPathLength)
    print("Deformable part per path") 
    print(coverableLengthPerPath)
    print("Non deformable part per path: ") 
    print(nonDeformableLengthPerPath )
    #print("Minimum final length of the structure: ") 
    #print(finalLengthOfTheLongestPath)

    # Define a list with the final length of each path in case there is a complete sweep
    for i in range(numberOfPaths):
        if finalLengthOfTheLongestPath <= totalPathLength[i]:
            finalPathLength.append(finalLengthOfTheLongestPath)
        else:
            finalPathLength.append(totalPathLength[i])
            
    # Define a list with the final deformable part per path
    for i in range(numberOfPaths):  
        finalDeformablePartPerPath.append(totalPathLength[i]-finalPathLength[i])     
    
    # Animation time
    timeOfTheAnimation = max(finalDeformablePartPerPath )
    #listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i]   
    print("Final length of each path: ") 
    print(finalPathLength)
    print("Amount of material that has to deform: ") 
    print(finalDeformablePartPerPath )
    

    
    # Create a list with the distance per path from the very first node to the head nod eof each path
    for i in range(numberOfPaths):
        #if finalLengthOfTheLongestPath <= totalPathLength[i]:
        distancesFromTheFistNodeToTheHeadOfEachPath.append((abs(totalPathLength[i] - (coordinateOfTheVeryLastNode - coordinateOfTheVeryFirstNode )),i+1))
        #else:
            #ldistancesFromTheFistNodeToTheHeadOfEachPath.append((0,i+1))
    print("    ")
    print("Sequence per path: ") 
    print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)
    print("    ")
    
    #This loop define the final sequence with the corrected deformation
    oldLength = 0.0
    flag = 0
    for i in range(numberOfPaths):
        for j in range(listOfTheNumberOfDeformableMemberAndGaps[i]):
            if flag == 0:
                if finalDeformablePartPerPath[i] >= listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]:
                    finalDeformablePartPerPath[i] = finalDeformablePartPerPath[i] - listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]
                else: 
                    flag = 1
                    listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] = finalDeformablePartPerPath[i]
                    listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][2] = listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] / 10
                    listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5] =  100 * listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] / listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][4]
            else:
                listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5] = 0
                listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] = 0
                
        flag = 0    
    print("    ")
    
    print("Sequence per path: ") 
    print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)
    print("    ")
    
    #print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[0][0][3])
    #print("Distance from the first node to the head of each node: ") 
    #print(distancesFromTheFistNodeToTheHeadOfEachPath)
    
    #print(distancesFromTheFistNodeToTheHeadOfEachPath)
    #Clasify in what order the paths will start deforming
    #distancesFromTheFistNodeToTheHeadOfEachPath.sort()
    
    
    # Define the time in which each path will start deforming
    for i in range(numberOfPaths):
            listOfTheTimesOfEachPathWillStartDeforming.append(distancesFromTheFistNodeToTheHeadOfEachPath[i][0]/10)
    #print("List of the time in which each path will start deforming")
    #print(listOfTheTimesOfEachPathWillStartDeforming)
    # Define the number of the lonsgest path
    for i in range(numberOfPaths):
        if listOfTheTimesOfEachPathWillStartDeforming[i]==0:
            pathNumberOfTheLongestFinalPath = i+1
    
    #print("Value of the longest path")
    #print(lengthOfTheLongestPath )
    #print("Number of the longest path")
    #print(pathNumberOfTheLongestFinalPath)
    
    # Define the time in which each path will reach the longest non deformable part
    #for i in range(numberOfPaths):
        #timeOfEachPathToReachTheLengthOfTheLongestNonDeformablePart.append(listOfTheTimesOfEachPathWillStartDeforming[i] + abs(totalPathLength[i] - finalLengthOfTheLongestPath)/10)
    #print("List of the time in which each path will reach the longest non deformable part")
    #print(timeOfEachPathToReachTheLengthOfTheLongestNonDeformablePart)
    
    
    
    #for i in range(numberOfPaths):
        #listOfTheOrderInWhichThePathsWillStartDeforming.append(distancesFromTheFistNodeToTheHeadOfEachPath[i][1])
    
    #print("List of the order the paths will start deforming")     
    #print(listOfTheOrderInWhichThePathsWillStartDeforming)
    
    # Define the list of inclined members per Path
    for j in range(len(my_elements)):
            if my_elements[j].get_startingLoadpath() != my_elements[j].get_finalLoadpath():
                inclinedMemberListPerPath.append(my_elements[j])
    #####################################################################################        
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
    scn.frame_end = 10 + 50 + timeOfTheAnimation/10 #30 + abs(valueOfTheFurthestNodeThatBelongsToADeformableMember - valueOfTheNearestNodeThatBelongsToADeformableMember)/10
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
        bpy.context.scene.frame_current = 50
        cube.location[0] -= 500
        cube.keyframe_insert('location', frame = 50)
        fcurves = cube.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR' 
         
    # Move the elements of each path to the initial position    
    for i in range(numberOfPaths):
        time = listOfTheTimesOfEachPathWillStartDeforming[i] + 50
        for j in range(listOfTheNumberOfMembersInEachPath[i]):
            if finalLengthOfTheLongestPath <= finalPathLength[i]:
                cube = my_elements[horizontalMemberListPerPath[i][j][1]-1].get_member()
                bpy.context.scene.frame_current = time
                cube.location[0] -= distancesFromTheFistNodeToTheHeadOfEachPath[i][0]
                cube.keyframe_insert('location', frame = time)
                fcurves = cube.animation_data.action.fcurves
                for fcurve in fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'LINEAR' 
            else:
               cube = my_elements[horizontalMemberListPerPath[i][j][1]-1].get_member()
               bpy.context.scene.frame_current = 50 + coverableLengthPerPath[pathNumberOfTheLongestFinalPath-1]/10
               cube.location[0] -= coverableLengthPerPath[pathNumberOfTheLongestFinalPath-1]
               cube.keyframe_insert('location', frame = 50 + coverableLengthPerPath[pathNumberOfTheLongestFinalPath-1]/10)
               fcurves = cube.animation_data.action.fcurves
               for fcurve in fcurves:
                   for kf in fcurve.keyframe_points:
                       kf.interpolation = 'LINEAR'
                                  
    ########################################################################
    ###########Here starts the definition of variables and function to get the animation            
    #We are going to use the final length per path to determine th time
    #print(len(my_elements[20].get_member()))
    gg =0
    for i in range(numberOfPaths):
        timeOffset = 50 + listOfTheTimesOfEachPathWillStartDeforming[i]
        for j in range(listOfTheNumberOfDeformableMemberAndGaps[i]):
            if gg == 0:#finalLengthOfTheLongestPath <= totalPathLength[i]:
                cube = my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_member()
                positionOfNodeA = cube.location[0]
                inicio = timeOffset
                duration = listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][2]
                final = inicio + duration
                #print(inicio)
                #print(final)
                
                # Translate element  
                bpy.context.scene.frame_current = inicio
                cube.keyframe_insert('location', frame = inicio)
                bpy.context.scene.frame_current = final
                cube.location[0] = positionOfNodeA  - listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]/2#(1-(100 - my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_deformation())/100)*my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].calcLength()/2
                cube.keyframe_insert('location', frame = final)
                fcurves = cube.animation_data.action.fcurves
                for fcurve in fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'LINEAR'
                        
                
                # Deform the element
                bpy.context.scene.frame_current = inicio
                cube.keyframe_insert('scale', frame = inicio)
                bpy.context.scene.frame_current = final
                cube.scale[2] *= 1 - (listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5]/100)#(100 - my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_deformation())/100
                cube.keyframe_insert('scale', frame = final)
                fcurves = cube.animation_data.action.fcurves
                for fcurve in fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'LINEAR'
             
                
                timeOffset  = final 
                #print(listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][0])
                for p in range(listOfTheNumberOfMembersInEachPath[i]): 
                    if horizontalMemberListPerPath[i][p][1] == listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]:
                        for pp in range(listOfTheNumberOfMembersInEachPath[i]):
                            if  horizontalMemberListPerPath[i][p][2] < pp +1:
                                #print(horizontalMemberListPerPath[i][pp][2])
                                # Translation of the rest of the rest of the member of the path
                                elemento = my_elements[horizontalMemberListPerPath[i][pp][1]-1].get_member()
                                positionOfNodeAOfTheCurrentElement = elemento.location[0]
                                bpy.context.scene.frame_current = inicio
                                elemento.keyframe_insert('location', frame = inicio)
                                bpy.context.scene.frame_current = final
                                elemento.location[0] = positionOfNodeAOfTheCurrentElement - listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]#(1-(100 - my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_deformation())/100)*my_elements[listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].calcLength()
                                elemento.keyframe_insert('location', frame = final)
                                fcurves = elemento.animation_data.action.fcurves
                                for fcurve in fcurves:
                                    for kf in fcurve.keyframe_points:
                                        kf.interpolation = 'LINEAR'
                                        
        
        
        timeOffset = 50
        print("   ")
        
#Delete everything
myHeader.initialize()
#Call the main function
main()
#Start animation
#bpy.ops.screen.animation_play(reverse=False, sync=False) 
# draw node
# draw node
