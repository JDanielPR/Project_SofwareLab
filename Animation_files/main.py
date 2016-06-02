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
from math import fabs
from operator import itemgetter # to use max
import myHeader
import colores
import setCamera
import setLamp
import mathutils
import Node
import Element
import Structure
import Wall
import ReadInput

# Define main function
def main():
    print("The program starts here")
    imp.reload(myHeader)   #Load library
    imp.reload(Node)       #Load library
    imp.reload(setCamera)  #Load library
    imp.reload(setLamp)    #Load library
    imp.reload(Element)    #Load library
    imp.reload(Structure)  #Load library
    imp.reload(Wall)       #Load library
    imp.reload(ReadInput)  #Load library
    myHeader.delete_all()  #Clean everything
    # Create an object to read
    reader = ReadInput.ReadTxt("C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\Animation_files\Example8.txt")
    (listOfNodes, listOfElements, numberOfNodes, numberOfElements, numberOfHorizontalLevels) = reader.getInformation()
    # Define the list of nodes and member 
    my_structure  = Structure.Structure(listOfNodes, listOfElements, numberOfNodes, numberOfElements, numberOfHorizontalLevels) 
    # Create an object wall
    widthOfWall = fabs(my_structure.get_locationOfTheLastPath() - my_structure.get_locationOfTheFirstPath())
    my_Wall = Wall.Wall(my_structure.get_coordinateOfTheVeryFirstNode(), my_structure.get_locationOfTheFirstPath() , widthOfWall)
    my_Wall.build_wall()
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = 10 + 50 + my_structure.get_timeOfTheAnimation()/10 
    scn.frame_step = 1
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    scn.render.resolution_percentage = 100
    scn.render.use_antialiasing = False
    scn.render.use_full_sample = False
    scn.render.image_settings.file_format = 'AVI_RAW' 
    scn.render.filepath = 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\red.avi'
    setLamp.setLamp(scn,my_structure.get_coordinateOfTheVeryFirstNode(),my_structure.get_locationOfTheFirstPath() + widthOfWall/2,-200) ##300 150
    setCamera.setCamera(scn , my_structure.get_coordinateOfTheVeryFirstNode(), my_structure.get_locationOfTheFirstPath() + widthOfWall/2, -1500, 15) #(576, 150, -1500, 20) 
    #bpy.ops.render.render(animation=True)
    #Scenename = 'Scene' 
    #bpy.data.scenes[Scenename].render.resolution_x = 1280
    #bpy.data.scenes[Scenename].render.resolution_y = 720
    #bpy.data.scenes[Scenename].render.resolution_percentage = 100
    #bpy.data.scenes[Scenename].render.frameStep= 1
    #bpy.data.scenes[Scenename].render.image_settings.file_format = 'AVI_JPEG' 
    #bpy.data.scenes[Scenename].render.filepath = 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\red.avi'


    
    
    
#Delete everything
myHeader.initialize()
scene = bpy.context.scene
for obj in scene.objects:
    scene.objects.unlink(obj)

# clear everything for now

#Call the main function
main()
#Start animation
#bpy.ops.screen.animation_play(reverse=False, sync=False) 


# Cycles sampling
#bpy.data.scenes[Scenename].cycles.samples = 200

# stamp
#bpy.data.scenes[Scenename].render.use_stamp = 1
#bpy.data.scenes[Scenename].render.stamp_background = (0,0,0,1)

#Scenename = 'Scene'
#bpy.data.scenes[Scenename].render.resolution_x = 1280
#bpy.data.scenes[Scenename].render.resolution_y = 720
#bpy.data.scenes[Scenename].render.resolution_percentage = 100
#bpy.data.scenes[Scenename].render.use_antialiasing = True
#bpy.data.scenes[Scenename].render.use_full_sample = True
    # output
#bpy.data.scenes[Scenename].render.image_settings.file_format = 'AVI_JPEG' 
#bpy.data.scenes[Scenename].render.filepath = 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\red.avi'
#bpy.data.scenes[Scenename].render.use_placeholder = True
#bpy.data.scenes[Scenename].render.use_overwrite = False
    # start render animation
#bpy.ops.render.render(animation=True,scene=Scenename)





