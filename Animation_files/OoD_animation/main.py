import bpy   #Module for blender
import imp
import initialization
import Structure
import sys
import os

sys.path.append('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation')
import OoD_problem

# Define main function
def main():
    imp.reload(initialization)   #Load library
    imp.reload(Structure)
    imp.reload(sys)
    imp.reload(OoD_problem)
    imp.reload(os)
    
    #Delete everything
    initialization.initialize()
    initialization.delete_all()  #Clean everything
    
    struct = OoD_problem.Massimo.read_xml()
    [i_s,d_h] = struct.solve()
    myStructure = Structure.Structure(i_s , d_h[1])
    
    '''
    ################################################33
    file = os.path.abspath('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\graph.jpg')
    bpy.ops.import_image.to_plane(
    use_shadeless=True,
    files=[{'name': os.path.basename(file)}],
    directory=os.path.dirname(file))
    bpy.context.scene.objects.active.select = True
    bpy.context.object.dimensions = 100, 100, 0 
    bpy.context.object.location = -100, 200, 0 
    
    cube1 = bpy.data.objects["graph"]
            
    inicio = 0
    final  = 25
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= -140
    cube1.location[1] -= 150
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'   
                           
    # Deform the element
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('scale', frame = inicio)
    bpy.context.scene.frame_current = final
    bpy.ops.transform.resize(value=(0, 0, 0))
    cube1.keyframe_insert('scale', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
    ######################################################33       
    file = os.path.abspath('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\graph2.jpg')
    bpy.ops.import_image.to_plane(
    use_shadeless=True,
    files=[{'name': os.path.basename(file)}],
    directory=os.path.dirname(file))
    bpy.context.scene.objects.active.select = True
    bpy.context.object.dimensions = 100, 100, 0 
    bpy.context.object.location = 20, 200, 0 
    
    cube1 = bpy.data.objects["graph2"]
            
    inicio = 25
    final  = 50
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= -120
    cube1.location[1] -= 150
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'   
                           
    # Deform the element
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('scale', frame = inicio)
    bpy.context.scene.frame_current = final
    bpy.ops.transform.resize(value=(0, 0, 0))
    cube1.keyframe_insert('scale', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
    #############################################33333333        
    file = os.path.abspath('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\graph.jpg')
    bpy.ops.import_image.to_plane(
    use_shadeless=True,
    files=[{'name': os.path.basename(file)}],
    directory=os.path.dirname(file))
    bpy.context.scene.objects.active.select = True
    bpy.context.object.dimensions = 100, 100, 0 
    bpy.context.object.location = 140, 200, 0 
    
    cube1 = bpy.data.objects["graph"]
            
    inicio = 50
    final  = 75
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= 90
    cube1.location[1] -= 200
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'   
                           
    # Deform the element
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('scale', frame = inicio)
    bpy.context.scene.frame_current = final
    bpy.ops.transform.resize(value=(0, 0, 0))
    cube1.keyframe_insert('scale', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
    ################################33
    
    file = os.path.abspath('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\graph2.jpg')
    bpy.ops.import_image.to_plane(
    use_shadeless=True,
    files=[{'name': os.path.basename(file)}],
    directory=os.path.dirname(file))
    bpy.context.scene.objects.active.select = True
    bpy.context.object.dimensions = 100, 100, 0 
    bpy.context.object.location = 260, 200, 0 
    
    cube1 = bpy.data.objects["graph2"]
            
    inicio =75
    final  = 100
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('location', frame = inicio)
    bpy.context.scene.frame_current = final
    cube1.location[0] -= 110
    cube1.location[1] -= 200
    cube1.keyframe_insert('location', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'   
                           
    # Deform the element
    bpy.context.scene.frame_current = inicio
    cube1.keyframe_insert('scale', frame = inicio)
    bpy.context.scene.frame_current = final
    bpy.ops.transform.resize(value=(0, 0, 0))
    cube1.keyframe_insert('scale', frame = final)
    fcurves = cube1.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'
            '''
main()






