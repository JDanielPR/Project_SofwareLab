import setCamera
import setLamp
import imp
import bpy   #Module for blender
import os
import Color
from bpy import context
  
imp.reload(setCamera)
imp.reload(setLamp)
imp.reload(Color)
# Define main function
def Parameters(numberOfFrames, width, height, pathDirectory):
    # Create background
    bpy.ops.mesh.primitive_plane_add(location=(width/2, -height /2 ,-100))  
    plane = bpy.context.object  
    plane.dimensions = (width *4, height *4, 0)
    plane.name = "Background" 
    Color.setColor(plane, Color.white)
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = numberOfFrames
    scn.frame_step = 1
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    scn.render.pixel_aspect_x = 0
    scn.render.pixel_aspect_y = 0
    scn.render.resolution_percentage = 100
    scn.render.use_antialiasing = False
    scn.render.use_full_sample = False
    scn.render.image_settings.file_format = 'H264'#'AVI_RAW' 
    scn.render.filepath = pathDirectory
    setLamp.setLamp(scn,width/2 ,-height/2, width * 2 )
    setCamera.setCamera(scn , width/2, -height/2, width * 2, height / 2)
    #bpy.ops.render.render(animation=True)