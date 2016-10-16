import bpy

def setLamp(scene, x, y ,z):
    scene.camera = None  
    scene = bpy.context.scene
    lamp_data = bpy.data.lamps.new(name="lamp", type='SUN')  
    lamp_object = bpy.data.objects.new(name="Lamp", object_data=lamp_data)  
    scene.objects.link(lamp_object)  
    lamp_object.location = (x,y,z)  
    lamp_object.rotation_euler = (0,0,0)
    lamp_data.use_specular =False