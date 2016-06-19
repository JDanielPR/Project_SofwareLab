import bpy   #Module for blender
import math
import imp
import random
from bpy import context
from mathutils import Vector
from math import pi
from math import fabs
from operator import itemgetter # to use max
import initialization
import setCamera
import setLamp
import mathutils
import Node
import Element
import Structure
import Wall
import ReadInput
import os


# Define main function
def main():
    imp.reload(initialization)   #Load library
    imp.reload(Node)             #Load library
    imp.reload(setCamera)        #Load library
    imp.reload(setLamp)          #Load library
    imp.reload(Element)          #Load library
    imp.reload(Structure)        #Load library
    imp.reload(Wall)             #Load library
    imp.reload(ReadInput)        #Load library
    initialization.delete_all()  #Clean everything
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
    

    '''
    file = os.path.abspath('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\Videos\\BMW.jpg')
    bpy.ops.import_image.to_plane(
    use_shadeless=True,
    files=[{'name': os.path.basename(file)}],
    directory=os.path.dirname(file))
    bpy.context.scene.objects.active.select = True
    bpy.context.object.dimensions = 4000, 2000, 0 
    bpy.context.object.location = 900, 200, 0 
    
    cube1 = bpy.data.objects["BMW"]
    # Translate element  
    inicio = 10
    final  = 50
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= 500
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
            
    inicio = 50
    final  = 140
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= 300
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'   
                           
    # Deform the element
    inicio = 50
    final  = 140
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('scale', frame = inicio)
    bpy.context.scene.frame_current = final
    bpy.ops.transform.resize(value=(0.5, 1.0, 1))
    cube1.keyframe_insert('scale', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:L
            kf.interpolation = 'LINEAR'
    '''        
    #bpy.ops.render.render(animation=True)
    
    
#Delete everything
os.system('cls') 
initialization.initialize()
scene = bpy.context.scene
for obj in scene.objects:
    scene.objects.unlink(obj)

##############################################################
# Clear default scene
#   - could not get animation to work when starting from new scene
#
#scene = Scene.GetCurrent() 
#for ob in scene.objects:
#   print ob.getName()
#   if ((cmp(ob.getName(),'Cube')==0) |
#       (cmp(ob.getName(),'Camera')==0) |
#    (cmp(ob.getName(),'Lamp')==0)):
#  scene.objects.unlink(ob)
##############################################################
#Call the main function
main()
#Start animation
#bpy.ops.screen.animation_play(reverse=False, sync=False) 

#reader = ReadInput.ReadArray("C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\Animation_files\Example1.txt")
#(listOfNodes, listOfElements, numberOfNodes, numberOfElements, numberOfHorizontalLevels) = reader.getInformation()
#print(listOfNodes)
#print(listOfElements)
#print(numberOfNodes)
#print(numberOfElements)
#print(numberOfHorizontalLevels)


