import bpy

def setCamera(scene, locationOfCamera, lents):
    '''Creates and configure the camera
    
    Args: 
        scene:
            bpy.context.scene, contains the scene of the video
        locationOfCamera:
            coordinates of the camera (x,y,z)
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    scene.camera = None 
    # Create the camera
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="Camera", object_data=cam_data)  
    scene.objects.link(cam_ob) 
    # Set the location of the camera 
    cam_ob.location = locationOfCamera
    # Set the rotation of the camera 
    cam_ob.rotation_euler = (0,0,0)
    cam = bpy.data.cameras[cam_data.name]  
    # Set the lents of the camera
    cam.lens = lents
    cam.sensor_width = lents
    # Set the type of camera
    cam.type = 'ORTHO'
    cam.lens_unit = 'MILLIMETERS'
    cam.ortho_scale = lents * 10
    # Set the zoom of the camera
    cam.clip_start = 0 
    cam.clip_end = 900
    cam_data.clip_start = 0
    cam_data.clip_end = 1580
    bpy.context.scene.camera = cam_ob
    