import bpy   # Module for blender
import os    # Module for console

def initialize():
    os.system('cls') # Clean console
    # gather list of items of interest.
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    # select them only.
    for object_name in candidate_list:
        bpy.data.objects[object_name].select = True  

    # Remove all selected.
    bpy.ops.object.delete()

    bpy.ops.object.select_by_type(type = 'MESH')
    bpy.ops.object.delete(use_global=False)
    for item in bpy.data.meshes:
        item.user_clear() # make it have zero users 
        bpy.data.meshes.remove(item)
        
    scene = bpy.context.scene
    for obj in scene.objects:
        scene.objects.unlink(obj)
        
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)

# This function define the static variable useful to name all the elements
x=0
def static_numberOfElement() :
   global x
   x=x+1
   return x
    
