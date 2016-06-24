import bpy

def setMovement(object, initialFrame, finalFrame , distance):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('location', frame = initialFrame)
    object.location[0] -= distance
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('location', frame = finalFrame)

    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
            
def setDeformation(object, initialFrame, finalFrame , amount):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    object.scale[2] *= 1 - amount#/100
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)

    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
            
def setColor(object, initialFrame, finalFrame):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('color', frame = initialFrame)
    bpy.context.scene.objects.active = object #active the object that you want to set the object color
    bpy.context.object.active_material.use_object_color = True #active the object color option
    bpy.context.object.color = (0,1,0,0.5)#set the value of the object color
    object.keyframe_insert('color', frame = initialFrame+1)
 
def deleteTag(object, initialFrame, finalFrame):
    bpy.context.scene.frame_current = initialFrame
    object.keyframe_insert('scale', frame = initialFrame)
    object.scale[0] *= 0
    object.scale[1] *= 0
    object.scale[2] *= 0
    bpy.context.scene.frame_current = finalFrame
    object.keyframe_insert('scale', frame = finalFrame)

    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'            