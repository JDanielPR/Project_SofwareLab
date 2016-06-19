import bpy
import sys
import math
from operator import itemgetter          #To sort list
from abc import ABCMeta, abstractmethod

class ReadInput:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getInformation(self): pass

class ReadTxt(ReadInput):
    def __init__(self , filename):
        try:
            self.file = open(filename, "r")
        except:
            print('There is no file named')
            sys.exit(0)
        
    def getInformation(self):
        numberOfNodes = int(self.file.readline())
        numberOfElements = int(self.file.readline())
        numberOfHorizontalLevels =int(self.file.readline())
    
        genericList= []
        nodes = []
        elements = []
    
        genericList= self.file.read().split()
        self.file.close()
        k = 0
        for i in range(numberOfNodes + numberOfElements ):
            if i < numberOfNodes:
                nodes.append([])
                for j in range(3*(i+1)-3,3*(i+1)):
                    nodes[i].append(float(genericList[j])) 
                k =  3*(i+1)
            else:
                elements.append([])
                for j in range(k, k + 7):
                    elements[i - numberOfNodes].append(float(genericList[j]))
                k = k + 7     
        return (nodes, elements , numberOfNodes, numberOfElements, numberOfHorizontalLevels)

class ReadArray(ReadInput):
    def __init__(self , filename):
        self.file = open(filename, "r") 
        
    def getInformation(self):
        numberOfNodes = 0
        numberOfElements = 0
        numberOfHorizontalLevels = 0
        genericList= []
        members = []
        nodes = []
        elements = []
        horizontalMembers = []
        inclinedMembers = []
        listOfelementsPerPath = []
        listOfTheNumberOfMembersPerPath = []
        listOfNodesXCoordinates_old = []
        listOfNodesXCoordinates_new = []
        listOfElements_old = []

        genericList= self.file.read().split()
        self.file.close()
        # Create a list of the information of each member
        for i in range(int(len(genericList)/5)):
            members.append([])
            for j in range(i*5,i*5+5):
                members[i].append(genericList[j]) 
        # Clasify in horizontal or oriented members
        for i in range(int(len(genericList)/5)):
            members[i].append(list(members[i][0])[0]) #Add id
            members[i].append(list(members[i][0])[1]) #Add level
            members[i].append(list(members[i][0])[2]) #Add position in loadpath
            members[i].remove(members[i][0])          #Remove old tag
            if members[i][4] == 'e':                  #Clasify whether is horizontal or inclined member
                horizontalMembers.append(members[i])
                members[i].remove(members[i][4])
            elif members[i][4] == 'x':
                inclinedMembers.append(members[i])
                members[i].remove(members[i][4])
        # Conversion to int of the horizontal members information
        for i in range(len(horizontalMembers)):
            for j in range(6):
                horizontalMembers[i][j] = int(horizontalMembers[i][j])
        # Conversion to int of the inclined members information
        for i in range(len(inclinedMembers)):
            for j in range(6):
                inclinedMembers[i][j] = int(inclinedMembers[i][j])

        horizontalMembers.sort(key=lambda x: x[4]) 
        #Get the maximum number of levels
        numberOfHorizontalLevels = max([x[4] for x in horizontalMembers]) + 1
        #Clasify elements according to the loadpath
        for i in range(numberOfHorizontalLevels):
            listOfelementsPerPath.append([])
            for j in range(len(horizontalMembers)):
                if horizontalMembers[j][4] == i: 
                    listOfelementsPerPath[i].append(horizontalMembers[j])
        
        #Sort according to the position
        for j in range(numberOfHorizontalLevels):
            if listOfelementsPerPath[j] != []:
                listOfelementsPerPath[j].sort(key=lambda x: x[5])
                listOfTheNumberOfMembersPerPath.append(1 + max([x[5] for x in listOfelementsPerPath[j]]))
            else:
                listOfTheNumberOfMembersPerPath.append(0)
        
        #Get the coordinates of nodes
        for i in range(numberOfHorizontalLevels):
            listOfNodesXCoordinates_old.append([])
            for j in range(listOfTheNumberOfMembersPerPath[i]):
                if listOfelementsPerPath[i][j][2] != 0:  
                    listOfNodesXCoordinates_old[i].append(listOfelementsPerPath[i][j][0]) 
                    listOfNodesXCoordinates_old[i].append(int(listOfelementsPerPath[i][j][0] + math.fabs(listOfelementsPerPath[i][j][1] - listOfelementsPerPath[i][j][0]) - listOfelementsPerPath[i][j][2]))
                    listOfNodesXCoordinates_old[i].append(listOfelementsPerPath[i][j][1])
                else:
                    listOfNodesXCoordinates_old[i].append(listOfelementsPerPath[i][j][0])
                    listOfNodesXCoordinates_old[i].append(listOfelementsPerPath[i][j][1])
        
        #print(listOfNodesXCoordinates_old)
        # Merge with list of inclined members
        for i in range(len(inclinedMembers)):
            listOfNodesXCoordinates_old[inclinedMembers[i][4]].append(inclinedMembers[i][0])
            listOfNodesXCoordinates_old[inclinedMembers[i][5]].append(inclinedMembers[i][1])
        # Sort according to the position of the coordinate
        for j in range(numberOfHorizontalLevels):
            if listOfNodesXCoordinates_old[j] != []:
                listOfNodesXCoordinates_old[j].sort()
        
        #print(listOfNodesXCoordinates_old) 

        # Avoid repetition
        for i in range(numberOfHorizontalLevels):
            listOfNodesXCoordinates_new.append([])
            for j in listOfNodesXCoordinates_old[i]:
                if j not in listOfNodesXCoordinates_new[i]:
                    listOfNodesXCoordinates_new[i].append(j)
                    
        # Add coordinate in y                    
        counter = 1
        addLevel = 0 
        for i in range(numberOfHorizontalLevels):
            for j in listOfNodesXCoordinates_new[i]:
                nodes.append([counter , j, addLevel])
                counter = counter + 1
            addLevel = addLevel + 300    
        numberOfNodes = len(nodes)
        
        # Count the number of elements per path
        for i in range(numberOfHorizontalLevels):
           for j in range(listOfTheNumberOfMembersPerPath[i]):
               if listOfelementsPerPath[i][j][2] == 0:
                   numberOfElements = numberOfElements + 1
               else:
                   numberOfElements = numberOfElements + 2
        # Add inclined members
        for i in range(len(inclinedMembers)):
            if (inclinedMembers[i][2] == 0):
                numberOfElements = numberOfElements + 1
            else:
                numberOfElements = numberOfElements + 2
                
        # Add gaps
        for i in range(numberOfHorizontalLevels):
            if listOfTheNumberOfMembersPerPath[i] != 0:
                for j in range(listOfTheNumberOfMembersPerPath[i]-1):
                    if listOfelementsPerPath[i][j][1] != listOfelementsPerPath[i][j+1][0]:
                        numberOfElements = numberOfElements + 1
        
        #print(inclinedMembers)
        #print(listOfelementsPerPath)
        #print(horizontalMembers)
        #print(listOfTheNumberOfMembersPerPath)
        #print(listOfNodesXCoordinates_old)
        #print(listOfNodesXCoordinates_new)
        #print(numberOfElements)
        # Clasify elements
        '''
        for i in range(numberOfHorizontalLevels):
            listOfElements_old.append([])
            for j in listOfNodesXCoordinates_new[i]:
                listOfElements_old[i].append([listOfNodesXCoordinates_new[i][j],listOfNodesXCoordinates_new[i][j+1]])
                '''
        return (nodes, elements , numberOfNodes, numberOfElements, numberOfHorizontalLevels)
            