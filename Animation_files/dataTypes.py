from bpy import context

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