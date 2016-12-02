import imp
import bpy           
import os
from Visualization import setCamera     
from Visualization import setLamp       
from Visualization import setColor      
from bpy import context
  
imp.reload(setCamera)
imp.reload(setLamp)
imp.reload(setColor)

def Parameters(numberOfFrames, 
               resolution,
               locationWall,
               locationBackground,
               locationOfCamera,
               width, 
               height, 
               pathDirectory):
    '''Define the parameters of the render
    
    Args:
        numberOfFrames:
            integer, the number of frames of the animation.
        resolution:
            float, the resolution
        locationWall:
            coordinate of the position of the element which 
            represents the blue wall.
        locationBackground:
            coordinate of the position of the element which 
            represents the background.
        locationCamera:
            coordinate of the position of the camera.
        width:
            float, the width of the structure.
        height:
            float, the height of the structure.
        pathdirectory:
            string, path where the video will be store
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Create white background
    bpy.ops.mesh.primitive_plane_add(location = locationBackground) 
    plane = bpy.context.object  
    plane.dimensions = (width * 5, height * 5, 0)
    plane.name = "Background" 
    setColor.setColor(plane, setColor.white)
    # Create wall
    bpy.ops.mesh.primitive_plane_add(location = locationWall) 
    wall= bpy.context.object  
    wall.dimensions = (2 * width , height * 5, 10)
    wall.name = "Wall" 
    setColor.setColor(wall, setColor.blue)
    # Set animation start and stop
    scn = bpy.context.scene
    # Set the duration in frames of the video
    scn.frame_start = 0
    scn.frame_end = numberOfFrames + 5
    # Set number of frames per step
    scn.frame_step = 1
    # Set resolution of the video
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    # Set pixel aspect to zero
    scn.render.pixel_aspect_x = 0
    scn.render.pixel_aspect_y = 0
    # Set resolution of the video
    scn.render.resolution_percentage = resolution * 25
    # Set format of the video
    scn.render.image_settings.file_format = 'H264'
    # Set location of the new video
    scn.render.filepath = pathDirectory
    # Set tiles size to reduce rendering time
    scn.render.tile_x = 64
    scn.render.tile_y = 64
    # Turn off ray tracing to make the rendering faster
    scn.render.use_raytrace = False
    # Turn off antialising to make the rendering faster
    scn.render.use_antialiasing = False
    # Turn off full sample to make the rendering faster
    scn.render.use_full_sample = False
    # Turn off shadows to make the rendering faster
    scn.render.use_shadows = False
    # Set lamp parameters
    setLamp.setLamp(scn,width / 2 ,-height / 2 , width * 2)
    # Set Camera parameters
    setCamera.setCamera(scn, locationOfCamera , 3 * height / 4 )
    # Create video
    bpy.ops.render.render(animation=True)