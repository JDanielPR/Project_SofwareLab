import bpy
import math
from math import pi

def setCamera(scene, x, y, z, lents):
    #scene = bpy.context.scene
    scene.camera = None 
    # Set the camera
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
    scene.objects.link(cam_ob)  
    cam_ob.location = (x, y, z)  
    cam_ob.rotation_euler = (0,0,0)
    #cam_ob.scale = (self.scaleX, self.scaleY, self.scaleZ)  
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = lents
    cam.type = 'PERSP'
    cam.lens_unit = 'MILLIMETERS'
    #cam.shift_x = 0.15
    #cam.shift_y = -0.7
    cam.clip_start = 209
    cam.clip_end = 900
    cam_data.clip_start = 30#24
    cam_data.clip_end = 1580#1500
    bpy.context.scene.camera = cam_ob
    