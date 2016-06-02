import bpy
import math
from math import pi
  
def setLamp(scene, x, y ,z):
    #scene = bpy.context.scene
    scene.camera = None  
    #for obj in scene.objects:  
        #scene.objects.unlink(obj)
    scene = bpy.context.scene
    lamp_data = bpy.data.lamps.new(name="lampa", type='SUN')  
    lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)  
    scene.objects.link(lamp_object)  
    lamp_object.location = (x + 500,y,z)#(300, 150, -200)
    lamp_object.rotation_euler = (pi,0,0)