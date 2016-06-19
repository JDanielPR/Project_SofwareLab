import imp
import Member
import LoadPath

imp.reload(Member)              #Load library
imp.reload(LoadPath)

class Structure():
    def __init__(self, input):
        self.input = input
        self.numberOfMembers = len(input)
        self.listOfHorizontalMembers = []
        self.listOfInclinedMembers = []
        self.listOfHorizontalLoadPaths = []
        self.numberOfLoadPaths = 0
        self.coordinateOfTheLeftBoundary = 0
        self.coordinateOfTheLRightBoundary = 0
        
        # Clasify Members and create members
        for i in range(self.numberOfMembers):
            if input[i].name[0] == 'e':
                self.listOfHorizontalMembers.append(Member.horizontalMember(self.input[i].name,self.input[i].x1 ,self.input[i].x2 ,self.input[i].deformableLength))
            else:
                self.listOfInclinedMembers.append(Member.horizontalMember(self.input[i].name,self.input[i].x1 ,self.input[i].x2 ,self.input[i].deformableLength))
        
        self.listOfHorizontalMembers[0].move(200, 10, 50)
        self.listOfHorizontalMembers[0].deform(100, 50, 100)
        
        # Set number of Loadpaths
        listOfTheNumberOfLoadPaths = []
        for i in range(len(self.listOfHorizontalMembers)-1):
            listOfTheNumberOfLoadPaths.append(int(self.input[i].name[1]))
        self.numberOfLoadPaths = max(listOfTheNumberOfLoadPaths)   
        #print(self.numberOfLoadPaths)
        
        # Create loadpaths
        for i in range(self.numberOfLoadPaths):
            self.listOfHorizontalLoadPaths.append(LoadPath.horizontalLoadPath(i+1))
            for j in range(len(self.listOfHorizontalMembers)):
                if int(self.listOfHorizontalMembers[j].nameOfMember[1]) == i+1:
                    self.listOfHorizontalLoadPaths[i].addMember(self.listOfHorizontalMembers[j])
                    
        #for i in range(self.numberOfLoadPaths):
            #self.listOfHorizontalLoadPaths.append([]) 
            #for j in range(len(self.listOfHorizontalMembers)):
                #if int(self.listOfHorizontalMembers[j].nameOfMember[1]) == i+1:
                    #self.listOfHorizontalLoadPaths[i].append(self.listOfHorizontalMembers[j])
        print(self.listOfHorizontalLoadPaths[0].getNumberOfMembers())  
        print(self.listOfHorizontalLoadPaths[1].getNumberOfMembers())   
        print(self.listOfHorizontalLoadPaths[2].getNumberOfMembers())   
        print(self.listOfHorizontalLoadPaths[3].getNumberOfMembers())   
        print(self.listOfHorizontalLoadPaths[4].getNumberOfMembers())    

        # Get the coordinate of the node which is more the left
        listOfTheX1Coordinates = []
        for i in range(len(self.listOfHorizontalMembers)-1):
            listOfTheX1Coordinates.append(self.input[i].x1)
        self.coordinateOfTheLeftBoundary = min(listOfTheX1Coordinates)   
        #print(self.coordinateOfTheLeftBoundary)

        # Get the coordinate of the node which is more the right 
        listOfTheX2Coordinates = []
        for i in range(len(self.listOfHorizontalMembers)-1):
            listOfTheX2Coordinates.append(self.input[i].x2)
        self.coordinateOfTheRightBoundary = max(listOfTheX2Coordinates)   
        #print(self.coordinateOfTheRightBoundary)
                
        

