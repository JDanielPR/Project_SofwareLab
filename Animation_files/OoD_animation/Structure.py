import imp
import Member
import setRender

imp.reload(Member)              #Load library
imp.reload(setRender)

class Structure():
    def __init__(self, i_s, solution):
        self.listOfHorizontalMembers = []
        self.listOfFinalTimes = []
        self.listOfX1= []
        self.listOfX2= []
        self.listOfLevels = []
        
        
        # Clasify Members and create members
        for i in range(len(i_s)):
                self.listOfHorizontalMembers.append(Member.horizontalMember(i_s[i].name,i_s[i].x1,i_s[i].x2 ,i_s[i].defo_length, i_s[i].lp_level))
                self.listOfX1.append(i_s[i].x1)
                self.listOfX2.append(i_s[i].x2)
                self.listOfLevels.append(i_s[i].lp_level)
        
        for i in range(len(self.listOfHorizontalMembers)):
            self.listOfHorizontalMembers[i].move(50, 0, 50)
            

        for i in range(len(self.listOfHorizontalMembers)):
            for j in range(len(solution[i_s[i]])):
                if solution[i_s[i]][j].transformation == 'm':
                    self.listOfHorizontalMembers[i].move(solution[i_s[i]][j].amount, solution[i_s[i]][j].frame_begin+50, solution[i_s[i]][j].frame_end+50)
                    self.listOfFinalTimes.append(solution[i_s[i]][j].frame_end+50)
                elif solution[i_s[i]][j].transformation == 'd':
                    self.listOfHorizontalMembers[i].deform(solution[i_s[i]][j].amount, solution[i_s[i]][j].frame_begin+50, solution[i_s[i]][j].frame_end+50)
                    self.listOfFinalTimes.append(solution[i_s[i]][j].frame_end+50)
                    
      

        totalTime = max(self.listOfFinalTimes)
        initialCoordinate = min(self.listOfX1)
        finalCoordinate = max(self.listOfX2)
        maxLevel = max(self.listOfLevels)
        print(initialCoordinate)
        print(finalCoordinate )
        print(maxLevel)
        setRender.Parameters(totalTime, initialCoordinate, finalCoordinate, maxLevel)
        
        