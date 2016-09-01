import bpy

# Function that set the frames where the displacement takes place
def setMovement(object, initialFrame, finalFrame , distance):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('location', frame = initialFrame)
    object.location[0] -= distance
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('location', frame = finalFrame)
    interpolation(object)

# Function that set the frames where the deformation takes place           
def setDeformation(object, initialFrame, finalFrame , amount):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    object.scale[2] *= 1 - amount
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)
    interpolation(object)

# Function that set the frames where the change of color takes place            
def setColor(object, initialFrame):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('color', frame = initialFrame)
    bpy.context.scene.objects.active = object 
    bpy.context.object.active_material.use_object_color = True 
    bpy.context.object.color = (0,1,0,0.5)
    object.keyframe_insert('color', frame = initialFrame + 1)

# Function that set the frames where the removal of the tag takes place 
def deleteTag(object, initialFrame, finalFrame):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    object.scale[0] *= 0
    object.scale[1] *= 0
    object.scale[2] *= 0
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)
    interpolation(object)

# Funtion for a linear interpolation               
def interpolation(object):
    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR' 

    
