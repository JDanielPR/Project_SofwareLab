import bpy

def setCamera(scene, x, y, z, lents):
    #scene = bpy.context.scene
    scene.camera = None 
    # Set the camera
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Camera", object_data=cam_data)  
    scene.objects.link(cam_ob)  
    cam_ob.location = (x, y, z)  
    cam_ob.rotation_euler = (0,0,0)
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = lents
    cam.sensor_width = lents
    cam.type = 'ORTHO'#'PERSP'
    cam.lens_unit = 'MILLIMETERS'
    cam.ortho_scale = lents * 10
    cam.clip_start = 30 
    cam.clip_end = 900
    cam_data.clip_start = 30
    cam_data.clip_end = 1580
    bpy.context.scene.camera = cam_ob
    