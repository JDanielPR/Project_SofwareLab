import bpy
import math
  
def setLamp(scene, x, y ,z):
    #scene = bpy.context.scene
    scene.camera = None  
    #for obj in scene.objects:  
        #scene.objects.unlink(obj)
    scene = bpy.context.scene
    lamp_data = bpy.data.lamps.new(name="lampa", type='SUN')  
    lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)  
    scene.objects.link(lamp_object)  
    lamp_object.location = (x,y,z)  
    lamp_object.rotation_euler = (0,0,0)
    lamp_data.use_specular =False