import setCamera
import setLamp
import imp
import bpy   #Module for blender
import os
from bpy import context
  
imp.reload(setCamera)
imp.reload(setLamp)
# Define main function
def Parameters(totalTime, initialCoordinate, finalCoordinate, maxLevel):
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = totalTime
    scn.frame_step = 1
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    scn.render.pixel_aspect_x = 0#maxLevel #3.4
    scn.render.pixel_aspect_y = 0#1.4
    scn.render.resolution_percentage = 100
    scn.render.use_antialiasing = False
    scn.render.use_full_sample = False
    scn.render.image_settings.file_format = 'H264'#'AVI_RAW' 
    scn.render.filepath = 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\Videos\\OoD.avi'
    setLamp.setLamp(scn,(finalCoordinate - initialCoordinate)/2 ,maxLevel/2,finalCoordinate+100)#,maxLevel,-200) ##300 150
    setCamera.setCamera(scn ,  (finalCoordinate- initialCoordinate)/2,maxLevel/2,finalCoordinate+100,30)#, maxLevel, -1500, 15) #(576, 150, -1500, 20) 
    #bpy.ops.render.render(animation=True)
    '''
    scene = context.scene
    path = 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\Videos'
    files = os.listdir(path)
    files.sort()

    # create the sequencer data
    scene.sequence_editor_create()

    seq = scene.sequence_editor.sequences.new_image(name="MyStrip",filepath=os.path.join(path, files[0]),channel=1, frame_start=1)
    #add the rest of the images.
    for f in files[1:int(totalTime)]:
        seq.elements.append(f)
    
    scn.render.image_settings.file_format = 'H264' 
    '''