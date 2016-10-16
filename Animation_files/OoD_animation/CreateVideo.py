import imp
import Member
import setRender
import initialization
#Load library
imp.reload(Member)              
imp.reload(setRender)
imp.reload(initialization)

class CreateVideo():
    def __init__(self, 
                 i_s, 
                 solution, 
                 verticalOffset, 
                 fps,  
                 pathDirectory):
                   
        self.listOfMembers = []
        # List to determine the duration of the video
        self.listOfFrames = []   
        # List to determine the coordinates X1            
        self.listOfX1= []   
        # List to determine the coordinates X2                    
        self.listOfX2= [] 
        # List to determine the number of paths                     
        self.listOfLevels = []   
        # This variable control the velocity of the video               
        self.fps = fps   
        # Location where the video will be stored                       
        self.pathDirectory = pathDirectory  
        # Distance between horizontal paths 
        self.verticalOffset = verticalOffset 
        # Prepare blender for a new video  
        initialization.initialize()             
        # Create members in Blender
        for i in range(len(i_s)):
                # Create members in Blender
                self.listOfMembers.append(Member.generalMember(i_s[i].name,
                                          i_s[i].x1,
                                          i_s[i].x2,
                                          i_s[i].defo_length, 
                                          i_s[i].lp_level1, 
                                          i_s[i].lp_level2, 
                                          self.verticalOffset, 
                                          i_s[i].mass_position))
                # Store coordinates and levels for setting the animation
                self.listOfX1.append(i_s[i].x1)
                self.listOfX2.append(i_s[i].x2)
                self.listOfLevels.append(i_s[i].lp_level2)
                # Create actions for each member
                for j in range(len(solution[i_s[i]])):
                    if solution[i_s[i]][j].transformation == 'd':
                        self.listOfMembers[i].deform(solution[i_s[i]][j].amount, 
                                                    (solution[i_s[i]][j].frame_begin)*self.fps, 
                                                    (solution[i_s[i]][j].frame_end)*self.fps)
                    else:
                        self.listOfMembers[i].move(solution[i_s[i]][j].amount, 
                                                  (solution[i_s[i]][j].frame_begin)*self.fps, 
                                                  (solution[i_s[i]][j].frame_end)*self.fps)
                    self.listOfFrames.append((solution[i_s[i]][j].frame_end)*self.fps)
        # Set parameter for creating the video                
        numberOfFrames = max(self.listOfFrames)
        width = max(self.listOfX2) - min(self.listOfX1)
        height = max(self.listOfLevels) * self.verticalOffset
        setRender.Parameters(numberOfFrames, 
                             width, 
                             height, 
                             self.pathDirectory)