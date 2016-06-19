import imp
import math
import bpy   #Module for blender
import Element
import Node
import Puntos

imp.reload(Node)              #Load library
imp.reload(Element)
imp.reload(Puntos)

class Structure():
    def __init__(self,my_nodes,my_elements, numberOfNodes, numberOfElements, numberOfPaths):
        self.numberOfNodes =    numberOfNodes
        self.numberOfElements = numberOfElements
        self.numberOfPaths =    numberOfPaths
        self.my_nodes = []                                     #Define nodes list
        self.my_elements = []                                  #Define memberslist
        self.coordinatesInX = []                               #List of all coordinates in x
        self.coordinatesInY = []                               #List of all coordinates in y
        self.coverableLengthPerPath = []                       #List of the maximum length that a load path can deform
        self.newCoverableLengthPerPath = []
        self.finalPathLength = []                              #List of the maximum length that a load path can reach
        self.horizontalMemberListPerPath = []                  #List of objects Members that are in horizontal position per path
        self.horizontalDeformableMemberListPerPath = []        #List of objects Members that are deformable in horizontal position per path
        self.inclinedMemberListPerPath = []                    #List of objects Memebers that are in inclined position
        self.distancesFromTheFistNodeToTheHeadOfEachPath = []
        self.finalDeformablePartPerPath = []
        self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming = []
        self.listOfGapsPerPath = []
        self.listOfTheNumberOfGapsPerPath = []
        self.listOfTheDeformablepartReminder = []
        self.listOfValueOfTheNearestNodeThatBelongsToADeformableMember = []
        self.listOfTheNumberOfMembersInEachPath = []
        self.listOfTheNumberOfDeformableMemberAndGaps = []
        self.listOfTheTimesOfEachPathWillStartDeforming = []
        self.nonDeformableLengthPerPath = []
        self.totalPathLength = []   
        self.inclinedMemberList = []                           #List of the lengths per path
        self.coordinateOfTheVeryFirstNode = 0
        self.coordinateOfTheVeryLastNode = 0
        self.locationOfTheFirstPath = 0
        self.locationOfTheLastPath = 0
        self.finalLengthOfTheLongestPath = 0
        self.lengthOfTheLongestPath = 0
        self.pathNumberOfTheLongestFinalPath = 0
        self.valueOfTheFurthestNodeThatBelongsToADeformableMember = 0
        self.valueOfTheNearestNodeThatBelongsToADeformableMember = 0
        self.timeOfTheAnimation = 0
        self.listaDeNodos = []
        
        self.positionoFNodes1= []
        self.positionoFNodes2= []
        self.positionoFNodes3= []

        # Sort the list of nodes according to the number of node
        my_nodes.sort()
        
        # Create all node objects
        for i in range(self.numberOfNodes): 
            self.my_nodes.append(Node.Node(my_nodes[i][0], my_nodes[i][1], my_nodes[i][2]))
            self.coordinatesInX.append(my_nodes[i][1])
            self.coordinatesInY.append(my_nodes[i][2])
            #self.listaDeNodos.append(Puntos.Puntos(my_nodes[i][0], my_nodes[i][1], my_nodes[i][2]))
	    
        # Create all element objects
        for i in range(self.numberOfElements):
            self.my_elements.append(Element.Element( i + 1 ,self.my_nodes[int(my_elements[i][0])-1],self.my_nodes[int(my_elements[i][1])-1],my_elements[i][2], my_elements[i][3], my_elements[i][4], my_elements[i][5], my_elements[i][6]))     
    
        
        self.coordinateOfTheVeryFirstNode = min(self.coordinatesInX)
        self.coordinateOfTheVeryLastNode  = max(self.coordinatesInX)
        self.locationOfTheFirstPath  = min(self.coordinatesInY)
        self.locationOfTheLastPath  = max(self.coordinatesInY)
        self.get_GapsPerPath()
        self.clasifyHorizontalElements()
        self.get_listOfValuesOfTheNearestNodeOfEachPath()
        self.valueOfTheFurthestNodeThatBelongsToADeformableMember = max(max(self.horizontalMemberListPerPath))[0] 
        self.valueOfTheNearestNodeThatBelongsToADeformableMember = (min(self.listOfValueOfTheNearestNodeThatBelongsToADeformableMember))[0] 
        self.enumerateMemberOfAPathLocally()
        self.finalLengthOfTheLongestPath = max(self.nonDeformableLengthPerPath )  #Final length of the complete system in
        self.lengthOfTheLongestPath = max(self.totalPathLength)
        self.get_finalPathLength()
        self.get_finalDeformablePartPerPath()
        self.get_distancesFromTheFistNodeToTheHeadOfEachPath()
        self.get_listOoD()
        self.get_listOfTheTimesOfEachPathWillStartDeforming()
        self.get_pathNumberOfTheLongestFinalPath()
        self.get_animation()

        
        # Define the list of inclined members per Path
        for j in range(len(my_elements)):
            if self.my_elements[j].get_levelOfNodeA() != self.my_elements[j].get_levelOfNodeB():
                self.inclinedMemberListPerPath.append(my_elements[j])
        
        #print(self.inclinedMemberListPerPath)
        #print(self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)
        #print(self.positionoFNodes1)
        #print(self.positionoFNodes2)
    ############################################################################
    def get_numberOfNodes(self): 
        return self.numberOfNodes
		
    def get_numberOfElements(self):
        return self.numberOfElements
		
    def get_numberOfPaths(self):
        return self.numberOfPaths
		
    def get_my_nodes(self):
        return self.my_nodes
		
    def get_my_elements(self):
        return self.my_elements
    
    def get_my_nodes(self):
        return self.my_nodes
		
    def get_locationOfTheFirstPath(self):
        return self.locationOfTheFirstPath 
    
    def get_locationOfTheLastPath(self):
        return self.locationOfTheLastPath 
	
    def get_GapsPerPath(self):
        # Sorting of gaps per path
        for i in range(self.numberOfPaths):
            countGaps = 0
            self.listOfGapsPerPath.append([])
            for j in range(self.numberOfElements):
                if self.my_elements[j].get_levelOfNodeA() == self.my_elements[j].get_levelOfNodeB():
                    if self.my_elements[j].get_levelOfNodeA() == i + 1:
                        if self.my_elements[j].get_elementType() == 2:
                            countGaps = countGaps + 1
                            self.listOfGapsPerPath[i].append([self.my_nodes[int(self.my_elements[j].get_nodeA()-1)].get_xCoordinate(), self.my_elements[j].get_numberOfElement() ])          
            self.listOfTheNumberOfGapsPerPath.append(countGaps)
     
        # Sort the gaps according to the distance to the wall
        for i in range(self.numberOfPaths):
            self.listOfGapsPerPath[i].sort()
    
    def clasifyHorizontalElements(self):
        # Clasify member according to the path
        l = 0
        k = 0 
        countElements = 0  
        countDeformableElementsAndGaps = 0 
        localNumerationPerPath = 0
        
        for i in range(self.numberOfPaths):
            self.horizontalMemberListPerPath.append([])             # Clasify members according to the path
            self.horizontalDeformableMemberListPerPath.append([])   # Clasify deformable members according to the path
            self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming.append([])
            numberMaxOfGaps = self.listOfTheNumberOfGapsPerPath[i]
            for j in range(self.numberOfElements):
                if self.my_elements[j].get_levelOfNodeA() == self.my_elements[j].get_levelOfNodeB():
                    if self.my_elements[j].get_levelOfNodeA() == i + 1:
                        self.horizontalMemberListPerPath[i].append([self.my_nodes[int(self.my_elements[j].get_nodeA() )-1].get_xCoordinate() , self.my_elements[j].get_numberOfElement(), localNumerationPerPath ])
                        countElements = countElements + 1
                        # Define length per path
                        l = self.my_elements[j].computeLength() + l
                        if self.my_elements[j].get_elementType() == 0 or self.my_elements[j].get_elementType() == 2:
                            k = self.my_elements[j].computeLength()*(self.my_elements[j].get_deformationPercentage()/100)+ k
                            self.horizontalDeformableMemberListPerPath[i].append(self.my_elements[j])
                            countDeformableElementsAndGaps = countDeformableElementsAndGaps + 1
                            if self.my_elements[j].get_elementType() == 0:
                                self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].append([self.my_elements[j].get_orderOfDeformation() + numberMaxOfGaps ,self.my_elements[j].get_numberOfElement(),self.my_elements[j].computeLength()*(self.my_elements[j].get_deformationPercentage()/100)/10, self.my_elements[j].computeLength()*(self.my_elements[j].get_deformationPercentage()/100), self.my_elements[j].computeLength() ,self.my_elements[j].get_deformationPercentage()])              
                            else:
                                self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].append([self.my_elements[j].get_orderOfDeformation() , self.my_elements[j].get_numberOfElement(),self.my_elements[j].computeLength()*(self.my_elements[j].get_deformationPercentage()/100)/10, self.my_elements[j].computeLength()*(self.my_elements[j].get_deformationPercentage()/100), self.my_elements[j].computeLength() ,self.my_elements[j].get_deformationPercentage()])  
            self.listOfTheNumberOfDeformableMemberAndGaps.append(countDeformableElementsAndGaps)
            self.listOfTheNumberOfMembersInEachPath.append(countElements)
            self.totalPathLength.append(l)          # Total length of the path
            self.coverableLengthPerPath.append(k)   # Length to cover including gaps
            l = 0
            k = 0
            countElements = 0
            countDeformableElementsAndGaps = 0
            localNumerationPerPath = 0
        
        
        # Once knowing the members of each path we proceed to clasify accornding to the position in the path
        for i in range(self.numberOfPaths):
            self.horizontalMemberListPerPath[i].sort()
            self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i].sort() 
            self.nonDeformableLengthPerPath.append(self.totalPathLength[i] - self.coverableLengthPerPath[i])  
            
        for j in range(self.numberOfElements):
            if self.my_elements[j].get_levelOfNodeA() != self.my_elements[j].get_levelOfNodeB():
                self.inclinedMemberList.append([self.my_elements[j].get_numberOfElement(),self.my_elements[j].computeLength()])           
        
        
        
        
    def get_listOfValuesOfTheNearestNodeOfEachPath(self):
         for i in range(self.numberOfPaths):
            if len(self.horizontalMemberListPerPath[i]) > 0:
                self.listOfValueOfTheNearestNodeThatBelongsToADeformableMember.append(self.horizontalMemberListPerPath[i][0]) 

    def enumerateMemberOfAPathLocally(self):
        # Enumarate the member of a path locally
        n = 1
        for i in range(self.numberOfPaths):
            for j in range(self.listOfTheNumberOfMembersInEachPath[i]):
                self.horizontalMemberListPerPath[i][j][2] = n
                n =  n + 1
            n = 1 
		    
    def get_finalPathLength(self):
        # Define a list with the final length of each path in case there is a complete sweep
        for i in range(self.numberOfPaths):
            if self.finalLengthOfTheLongestPath <= self.totalPathLength[i]:
                self.finalPathLength.append(self.finalLengthOfTheLongestPath)
            else:
                self.finalPathLength.append(self.totalPathLength[i])
		
    def get_finalDeformablePartPerPath(self):
        # Define a list with the final deformable part per path
        for i in range(self.numberOfPaths): 
            self.finalDeformablePartPerPath.append(self.totalPathLength[i]- self.finalPathLength[i])     
        self.timeOfTheAnimation = max(self.finalDeformablePartPerPath)
		
		
    def get_distancesFromTheFistNodeToTheHeadOfEachPath(self):
        # Create a list with the distance per path from the very first node to the head nod eof each path
        for i in range(self.numberOfPaths):
            self.distancesFromTheFistNodeToTheHeadOfEachPath.append((abs(self.totalPathLength[i] - (self.coordinateOfTheVeryLastNode - self.coordinateOfTheVeryFirstNode )),i+1))
        
        counter = 0
        for i in range(self.numberOfPaths):
            self.positionoFNodes1.append([]) 
            for j in range(self.numberOfNodes):
                if self.my_nodes[j].get_yCoordinate() == counter:
                    self.positionoFNodes1[i].append(self.my_nodes[j].get_xCoordinate())
            counter=counter+300
         
        #print(self.listOfTheNumberOfDeformableMemberAndGaps)
        for i in range(self.numberOfPaths):
            self.positionoFNodes2.append([]) 
            if self.listOfTheNumberOfDeformableMemberAndGaps[i] != 0:
                for j in range(len(self.positionoFNodes1[i])):
                    self.positionoFNodes2[i].append(self.positionoFNodes1[i][j]-500)
            else:
                self.positionoFNodes2[i].append(-500)
                
            
            

    def get_listOoD(self):
        #This loop define the final sequence with the corrected deformation
        oldLength = 0.0
        flag = 0
        for i in range(self.numberOfPaths):
            for j in range(self.listOfTheNumberOfDeformableMemberAndGaps[i]):
                if flag == 0:
                    if self.finalDeformablePartPerPath[i] >= self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]:
                        self.finalDeformablePartPerPath[i] = self.finalDeformablePartPerPath[i] - self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]
                    else: 
                        flag = 1
                        self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] = self.finalDeformablePartPerPath[i]
                        self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][2] = self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] / 10
                        self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5] =  100 * self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] / self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][4]
                else:
                    self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5] = 0
                    self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3] = 0
                
            flag = 0   
        aux = 0
        for i in range(self.numberOfPaths):
            for j in range(self.listOfTheNumberOfDeformableMemberAndGaps[i]):
                aux = aux + self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]
            self.newCoverableLengthPerPath.append(aux)
            aux = 0

    def get_listOfTheTimesOfEachPathWillStartDeforming(self):
        # Define the time in which each path will start deforming
        for i in range(self.numberOfPaths):
            self.listOfTheTimesOfEachPathWillStartDeforming.append(self.distancesFromTheFistNodeToTheHeadOfEachPath[i][0]/10)

    def get_pathNumberOfTheLongestFinalPath(self):
        # Define the number of the lonsgest path
        for i in range(self.numberOfPaths):
            if self.listOfTheTimesOfEachPathWillStartDeforming[i]==0:
                self.pathNumberOfTheLongestFinalPath = i+1
                
    def get_coordinateOfTheVeryFirstNode(self):
        return self.coordinateOfTheVeryFirstNode
    
    def get_timeOfTheAnimation(self):
        return self.timeOfTheAnimation
    
    def get_animation(self):
         
        # Set keyframes for Position XYZ value at Frame 1 and 10 (to hold position) for every cubes
        for i in range(self.numberOfElements):
            cube = self.my_elements[i].get_blenderElement()
            cube.keyframe_insert('location', frame=1)
            cube.keyframe_insert('location', frame=10) 
            


        #Move all the elements at the initial position  
        for i in range(self.numberOfElements):
            cube = self.my_elements[i].get_blenderElement()
            bpy.context.scene.frame_current = 50
            cube.location[0] -= 500
            cube.keyframe_insert('location', frame = 50)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR' 
        ##########################################

                    
        #######################################3333
        inicio = 50
        final = 90
        for i in range(len(self.inclinedMemberList)):
            cube = self.my_elements[int(self.inclinedMemberList[i][0])-1].get_blenderElement() 
            # Translate element  
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('location', frame = inicio)
            bpy.context.scene.frame_current = final
            cube.location[0] = cube.location[0]  - 400
            cube.keyframe_insert('location', frame = final)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
        
        inicio = 90
        final = 140
        for i in range(len(self.inclinedMemberList)):
            cube = self.my_elements[int(self.inclinedMemberList[i][0])-1].get_blenderElement() 
            # Translate element  
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('location', frame = inicio)
            bpy.context.scene.frame_current = final
            cube.location[0] = cube.location[0]  - 500
            cube.keyframe_insert('location', frame = final)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
        
        inicio = 140
        final = 170
        for i in range(len(self.inclinedMemberList)):
            cube = self.my_elements[int(self.inclinedMemberList[i][0])-1].get_blenderElement() 
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('scale', frame = inicio)
            bpy.context.scene.frame_current = final
            cube.scale[2] *= ((600)/(self.inclinedMemberList[i][1]/100))/100
            cube.keyframe_insert('scale', frame = final)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                     kf.interpolation = 'LINEAR'
                     
                 
        inicio = 140
        final = 170
        for i in range(len(self.inclinedMemberList)):
            cube = self.my_elements[int(self.inclinedMemberList[i][0])-1].get_blenderElement() 
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('rotation_euler', frame = inicio)
            cube.rotation_euler[2] =  math.atan(300/600)
            bpy.context.scene.frame_current = final
            cube.keyframe_insert('rotation_euler', frame = final)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                     kf.interpolation = 'LINEAR'
                     
        inicio = 140
        final = 170
        for i in range(len(self.inclinedMemberList)):
            cube = self.my_elements[int(self.inclinedMemberList[i][0])-1].get_blenderElement() 
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('location', frame = inicio)
            cube.location[0] = cube.location[0]  - 150
            bpy.context.scene.frame_current = final
            cube.keyframe_insert('location', frame = final)
            fcurves = cube.animation_data.action.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                     kf.interpolation = 'LINEAR'
            #Change color
            bpy.context.scene.frame_current = inicio
            cube.keyframe_insert('color', frame = inicio)
            bpy.context.scene.objects.active = cube #active the object that you want to set the object color
            bpy.context.object.active_material.use_object_color = True #active the object color option
            bpy.context.object.color = (0,1,0,0.5)#set the value of the object color
            cube.keyframe_insert('color', frame = final)
                                
        print(self.listOfTheTimesOfEachPathWillStartDeforming)
        ########################################################
        #print(self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming)          
        #print(self.coverableLengthPerPath)
        #print(self.newCoverableLengthPerPath)
        # Move the elements of each path to the initial position    
        for i in range(self.numberOfPaths):
            time = self.listOfTheTimesOfEachPathWillStartDeforming[i] + 50
            for j in range(self.listOfTheNumberOfMembersInEachPath[i]):
                if self.finalLengthOfTheLongestPath <= self.finalPathLength[i]:
                    cube = self.my_elements[self.horizontalMemberListPerPath[i][j][1]-1].get_blenderElement()
                    bpy.context.scene.frame_current = time
                    cube.location[0] -= self.distancesFromTheFistNodeToTheHeadOfEachPath[i][0]
                    cube.keyframe_insert('location', frame = time)
                    fcurves = cube.animation_data.action.fcurves
                    for fcurve in fcurves:
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR' 
                            
 

                else:
                    cube = self.my_elements[self.horizontalMemberListPerPath[i][j][1]-1].get_blenderElement()
                    bpy.context.scene.frame_current = 50 + self.newCoverableLengthPerPath[self.pathNumberOfTheLongestFinalPath-1]/10
                    cube.location[0] -= self.newCoverableLengthPerPath[self.pathNumberOfTheLongestFinalPath-1]
                    cube.keyframe_insert('location', frame = 50 + self.newCoverableLengthPerPath[self.pathNumberOfTheLongestFinalPath-1]/10)
                    fcurves = cube.animation_data.action.fcurves
                    for fcurve in fcurves:
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR'
                    
      
        
        for i in range(self.numberOfPaths):
            timeOffset = 50 + self.listOfTheTimesOfEachPathWillStartDeforming[i]
            for j in range(self.listOfTheNumberOfDeformableMemberAndGaps[i]):
                if self.finalLengthOfTheLongestPath <= self.finalPathLength[i]:
                    cube = self.my_elements[self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_blenderElement()
                    positionOfNodeA = cube.location[0]
                    #print(positionOfNodeA)
                    inicio = timeOffset
                    duration = self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][2]
                    final = inicio + duration
                
                    # Translate element  
                    bpy.context.scene.frame_current = inicio
                    cube.keyframe_insert('location', frame = inicio)
                    bpy.context.scene.frame_current = final
                    cube.location[0] = positionOfNodeA  - self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]/2
                    cube.keyframe_insert('location', frame = final)
                    fcurves = cube.animation_data.action.fcurves
                    for fcurve in fcurves:
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR'
                        
                    # Deform the element
                    bpy.context.scene.frame_current = inicio
                    cube.keyframe_insert('scale', frame = inicio)
                    bpy.context.scene.frame_current = final
                    cube.scale[2] *= 1 - (self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][5]/100)
                    cube.keyframe_insert('scale', frame = final)
                    fcurves = cube.animation_data.action.fcurves
                    for fcurve in fcurves:
                        for kf in fcurve.keyframe_points:
                            kf.interpolation = 'LINEAR'
                            
                    #Change color
                    bpy.context.scene.frame_current = inicio
                    cube.keyframe_insert('color', frame = inicio)
                    if self.my_elements[self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]-1].get_elementType() == 0:
                        bpy.context.scene.objects.active = cube #active the object that you want to set the object color
                        bpy.context.object.active_material.use_object_color = True #active the object color option
                        bpy.context.object.color = (0,1,0,0.5)#set the value of the object color
                    cube.keyframe_insert('color', frame = final)
                    #fcurves = cube.animation_data.action.fcurves
                    #for fcurve in fcurves:
                        #for kf in fcurve.keyframe_points:
                            #kf.interpolation = 'LINEAR'
                    
                    
                    timeOffset  = final 
                    
                    for p in range(self.listOfTheNumberOfMembersInEachPath[i]): 
                        if self.horizontalMemberListPerPath[i][p][1] == self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][1]:
                            for pp in range(self.listOfTheNumberOfMembersInEachPath[i]):
                                if  self.horizontalMemberListPerPath[i][p][2] < pp +1:
                                    # Translation of the rest of the rest of the member of the path
                                    elemento = self.my_elements[self.horizontalMemberListPerPath[i][pp][1]-1].get_blenderElement()
                                    self.positionOfNodeAOfTheCurrentElement = elemento.location[0]
                                    bpy.context.scene.frame_current = inicio
                                    elemento.keyframe_insert('location', frame = inicio)
                                    bpy.context.scene.frame_current = final
                                    elemento.location[0] = self.positionOfNodeAOfTheCurrentElement - self.listOfTheOrderInWhichTheMembersOfEachPathWillStartDeforming[i][j][3]
                                    elemento.keyframe_insert('location', frame = final)
                                    fcurves = elemento.animation_data.action.fcurves
                                    for fcurve in fcurves:
                                        for kf in fcurve.keyframe_points:
                                            kf.interpolation = 'LINEAR'
                                    

            timeOffset = 50
            

		

    
        
        
        