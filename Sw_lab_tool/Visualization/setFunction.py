import bpy
import math

def movement(object, initialFrame, finalFrame , amount, offset = 0):
    '''Set the frames where the displacement takes place
    
    Args:
        object:
            blender mesh, current object which will move
        initialFrame:
            integer, the starting frame of the movement
        finalFrame:
            integer, the final frame of the movement
        amount:
            float, amount of distance to move horizontally
        offset:
            float, amount of distance to move vertically
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set initial frame
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('location', frame = initialFrame)
    # Move object
    object.location[0] -= amount
    if offset:
        object.location[1] += offset 
    # Set final frame
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('location', frame = finalFrame)
    interpolation(object)

def rotation(object, initialFrame, finalFrame , amount):
    '''Set the frames where the rotation takes place
    
    Args:
        object:
            blender mesh, current object which will rotate
        initialFrame:
            integer, the starting frame of the rotation
        finalFrame:
            integer, the final frame of the rotation
        amount:
            float, amount of rotation
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set initial frame
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('rotation_euler', frame = initialFrame)
    # Rotate object
    object.rotation_euler[0] -= amount
    # Set final frame
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('rotation_euler', frame = finalFrame)
    interpolation(object)
        
def deformation(object, initialFrame, finalFrame , amount):
    '''Set the frames where the deformation takes place 
    
    Args:
        object:
            blender mesh, current object which will deform
        initialFrame:
            integer, the starting frame of the deformation
        finalFrame:
            integer, the final frame of the deformation
        amount:
            float, amount of deformation
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set initial frame
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    # Deform object
    object.scale[2] *= 1 - amount
    # Set final frame
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)
    interpolation(object)
       
def color(object, initialFrame, color):
    '''Set the frames where the change of color takes place   
    
    Args:
        object:
            blender mesh, current object which will color
        initialFrame:
            integer, the starting frame of the color
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set initial frame
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('color', frame = initialFrame)
    # Color object
    bpy.context.scene.objects.active = object 
    bpy.context.object.active_material.use_object_color = True 
    bpy.context.object.color = color
    # Set final frame
    object.keyframe_insert('color', frame = initialFrame + 1)

def elimination(object, initialFrame, finalFrame):
    '''Set the frames where the removal of the tag takes place 
    
    Args:
        object:
            blender mesh, current object which will vanish
        initialFrame:
            integer, the starting frame of the vanishing
        finalFrame:
            integer, the final frame of the vanishing
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set initial frame
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    # Delete object
    object.scale = ( 0, 0 ,0)
    # Set final frame
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)
    interpolation(object)
         
def interpolation(object):
    '''Linear interpolation 
    This interpolation makes the deformation and the movement smooth
    without any kind of acceleration 
    
    Args:
        object:
            blender mesh, current object 
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    # Set linear interpolation for actions of all the objects
    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR' 

    
