import bpy
import math
from math import pi

def setCamera(scene, width, length, height, lents):
    #scene = bpy.context.scene
    scene.camera = None 
    # Set the camera
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
    scene.objects.link(cam_ob)  
    cam_ob.location = (width + 900, length, height)  
    cam_ob.rotation_euler = (pi,0,0) 
    #cam_ob.scale = (self.scaleX, self.scaleY, self.scaleZ)  
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = lents
    cam.type = 'PERSP'
    cam.lens_unit = 'MILLIMETERS'
    #cam.shift_x = 0.15
    #cam.shift_y = 0.1
    cam.clip_start = 209
    cam.clip_end = 900
    cam_data.clip_start = 30#24
    cam_data.clip_end = 1580#1500
    bpy.context.scene.camera = cam_ob
    