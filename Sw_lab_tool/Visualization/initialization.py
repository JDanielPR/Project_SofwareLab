import bpy   # Module for blender
import os    # Module for console

def initialize():
    """Prepare Blender for anew animation
    Args:
        nothing is taken

    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    """
    os.system('cls') # Clean console
    # Gather list of items of interest.
    lObjects = [item.name for item in bpy.data.objects if item.type == "MESH"]
    # Select them only.
    for object_name in lObjects :
        bpy.data.objects[object_name].select = True  
    # Remove all selected.
    bpy.ops.object.delete()
    bpy.ops.object.select_by_type(type = 'MESH')
    bpy.ops.object.delete(use_global=False)
    for item in bpy.data.meshes:
        # Make it have zero users 
        item.user_clear() 
        bpy.data.meshes.remove(item)
    # Create variable to unlink objects from the scene
    scene = bpy.context.scene
    for obj in scene.objects:
        scene.objects.unlink(obj)
    # Delete name cameras or any other objects
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)

# This function define the static variable useful to name all the elements
x=0
def static_numberOfElement() :
   global x
   x=x+1
   return x
    
