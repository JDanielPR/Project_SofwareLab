import imp
import Member
import setRender
import bpy
import setAnimation

#Load library
imp.reload(Member)              
imp.reload(setRender)
imp.reload(setAnimation)

class Structure():
    def __init__(self, i_s, solution):
        self.listOfHorizontalMembers = []
        self.listOfFinalTimes = []
        self.listOfX1= []
        self.listOfX2= []
        self.listOfLevels = []
        self.offset = 0 # it is the tome when it finish translating into the wall
        self.fps = 1

        # Create members in Blender
        for i in range(len(i_s)):
                # Create horizontal members in Blender
                self.listOfHorizontalMembers.append(Member.horizontalMember(i_s[i].name,i_s[i].x1,i_s[i].x2 ,i_s[i].defo_length, i_s[i].lp_level))
                # Store coordinates and levels
                self.listOfX1.append(i_s[i].x1)
                self.listOfX2.append(i_s[i].x2)
                self.listOfLevels.append(i_s[i].lp_level)
        
        for i in range(len(self.listOfHorizontalMembers)):
            for j in range(len(solution[i_s[i]])):
                if solution[i_s[i]][j].transformation == 'm':
                    self.listOfHorizontalMembers[i].move(solution[i_s[i]][j].amount, (solution[i_s[i]][j].frame_begin+self.offset)*self.fps, (solution[i_s[i]][j].frame_end+self.offset)*self.fps)
                    self.listOfFinalTimes.append((solution[i_s[i]][j].frame_end+self.offset)*self.fps)
                elif solution[i_s[i]][j].transformation == 'd':
                    self.listOfHorizontalMembers[i].deform(solution[i_s[i]][j].amount, (solution[i_s[i]][j].frame_begin+self.offset)*self.fps, (solution[i_s[i]][j].frame_end+self.offset)*self.fps)
                    self.listOfFinalTimes.append((solution[i_s[i]][j].frame_end+self.offset)*self.fps)
         
        Member.inclinedMember('inclined',0, 100 ,100, 0, 1)
                    
        totalTime = max(self.listOfFinalTimes)
        initialCoordinate = min(self.listOfX1)
        finalCoordinate = max(self.listOfX2)
        maxLevel = max(self.listOfLevels)
        setRender.Parameters(totalTime, initialCoordinate, finalCoordinate, maxLevel)
        
        