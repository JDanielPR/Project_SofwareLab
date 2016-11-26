import imp
from Visualization import Member as e
from Visualization import setRender
from Visualization import initialization
import math as m
#Load library
imp.reload(e)              
imp.reload(setRender)
imp.reload(initialization)

class CreateVideo():
    def __init__(self, 
                 i_s, 
                 d_h, 
                 v_o, 
                 fps,  
                 resolution,
                 pathDirectory):
        '''Creates video in blender
    
        Args:
            i_s: 
                list, initial state
            d_h:
                dictionary, deformation history
            v_o: 
                integer, vertical offset-distance between horizontal paths
                Depending on the length of the elements this value can be
                varied by from 1 to 1000. For very short elements this
                ratio can have the value of 1. For complex structures
                this value can have up to 1000.
                Typical values are 1 and 50.
            fps: 
                float, animation speed. This value can vary from 0.1 to 4  
            resolution:
                integer, quality of the animation. The resolution affects
                the time in which the program will create the video in .avi
                The value is 1 is faster but the resolution is not good
                where as 4 is good enough with a relative good
                speed of video creation.
            path directory:
                path where the video will be stored
    
        Returns: 
            nothing is returned
    
        Raises:
            exceptions raised by the initial state
        '''  

        # List of Blender members objects             
        lMembers = []
        # List to determine the duration of the video
        listOfFrames = []   
        # List to determine the coordinates X1            
        listOfX1= []   
        # List to determine the coordinates X2                    
        listOfX2= [] 
        # List to determine the number of paths                     
        listOfLevels = []   
		# List to determine the number of steps for deformation of each element
        steps = []
        # Prepare blender for a new video  
        initialization.initialize() 
        
        for i in range(len(i_s)):
            # Create members in Blender according to the parameters
            lMembers.append(e.generalMember(i_s[i].name,
                                            i_s[i].x1,
                                            i_s[i].x2,
                                            i_s[i].defo_length, 
                                            i_s[i].lp_level1, 
                                            i_s[i].lp_level2, 
                                            v_o))
                                            #i_s[i].mass_position = 0))
            # Store coordinates and levels for setting the animation
            listOfX1.append(i_s[i].x1)
            listOfX2.append(i_s[i].x2)
            listOfLevels.append(i_s[i].lp_level2)
        
        # Width of the structure
        widthOfTheStructure =  max(listOfX2) - min(listOfX1)
        # Height of the structure
        heightOfTheStructure = max(listOfLevels) * v_o 
        # Distance to the wall
        distanceToTheWall = v_o + widthOfTheStructure 
		# Duration of pause in each steps
        pause = 0
        # Duration of the translation from origin to the wall
        transition = v_o + pause

        for i in d_h.keys():
            #Loop over the deformation history
            #Count the deformation steps of an element and store it
            #Note: There are elements which has 0 deformation steps
            try:
                deformationSteps = 0
                for j in range(len(d_h[i])):
                    if d_h[i][j].transformation == 'd':
                        deformationSteps = deformationSteps + 1
                steps.append(deformationSteps)
            except Exception:
                steps.append(0)
        
        for i in range(len(i_s)):
            #Loop over the initial state elements
            #Assign the actions to each element according to the step

            #Move each element of the structure to the wall
            #*initial frame
            #* final frame
            #* amount
            
            lMembers[i].move(pause, 
                            (transition - pause) * fps, 
                            distanceToTheWall - widthOfTheStructure )
            # Delta Y : Distance between loadpaths
            dY = v_o * (i_s[i].lp_level2 - i_s[i].lp_level1)
            # Delta X : Difference between the vertex of an element
            dX = i_s[i].x2 - i_s[i].x1
            # Initialize variables
            newDefoLength = i_s[i].defo_length
            oldDefoLength = i_s[i].defo_length
            newAngle      = m.atan(dY / dX)
            oldAngle      = m.atan(dY / dX)
            stepNumber    = 0      
            try:       
                for j in range(len(d_h[i_s[i]])):
                    # Assign to a variable an object from the d_h
                    s = d_h[i_s[i]][j]
                    lMembers[i].move((s.frame_begin + transition)* fps, 
                                     (s.frame_end   + transition)* fps, 
                                      0)
                    if s.transformation == 'd':
                        
                        #Deformation of the element
                        #To deform a member it is neccesary to know
                        #the frame in which the action takes place
                        #the frame in which the action finish
                        #the frames per second and the amount in
                        #which it deforms
                        #Note : It is necessary to know the state of 
                        #the angle and the length in each step
                        dX = dX - s.amount
                        if dX == 0:
                            newAngle = 0
                        else:
                            newAngle = m.atan(dY / dX)
                           
                        # Amount: Percentage of the original object to deform
                        newAmount     =  s.amount / newDefoLength 
                        newDefoLength =  newDefoLength - s.amount
                        stepNumber    =  stepNumber + 1
                        
                        lMembers[i].deform((s.frame_begin + transition) * fps, 
                                           (s.frame_end + transition) * fps,
                                            s.amount,
                                            newAmount,
                                            newAngle,
                                            oldAngle,
                                            newDefoLength,
                                            oldDefoLength,
										    stepNumber,
									        steps[i])

                        oldDefoLength  = newDefoLength 
                        oldAngle       = newAngle 
                    else:
                        
                        #Movement of the element
                        #To move a member it is neccesary to know
                        #the frame in which the action takes place
                        #the frame in which the action finish
                        #the frames per second and the amount in
                        #which it moves
                        lMembers[i].move((s.frame_begin + transition) * fps, 
                                         (s.frame_end   + transition) * fps,
                                          s.amount)
                                               
                    listOfFrames.append(s.frame_end * fps)
            except Exception:
                print(" ")

        # Number of frames 
        # Maximum number of frames + the time from the origin to the wall 
        if len(listOfFrames) == 0:
            numberOfFrames = transition * fps
        else:
            numberOfFrames = max(listOfFrames) + transition * fps
        
        # Location of the wall
        lwx =  min(listOfX1) - distanceToTheWall
        lwy = -heightOfTheStructure  / 2
        lwz =  10
        locationOfWall = (lwx, lwy, lwz)
        
        # Location of the background
        lbx =  widthOfTheStructure  / 2
        lby = -heightOfTheStructure / 2
        lbz = -100
        locationOfBackground = (lbx, lby, lbz)
        
        # Location of the camera
        lcx =  min(listOfX1) + 3 * widthOfTheStructure  / 8
        lcy = -heightOfTheStructure / 2
        lcz = 100
        locationOfCamera = (lcx, lcy, lcz)
        
        # Set Render function
        setRender.Parameters(numberOfFrames, 
                             resolution,
                             locationOfWall,
                             locationOfBackground,
                             locationOfCamera, 
                             widthOfTheStructure, 
                             heightOfTheStructure,
                             pathDirectory)