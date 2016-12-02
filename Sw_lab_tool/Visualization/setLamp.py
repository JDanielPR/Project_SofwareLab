import bpy

def setLamp(scene, x, y ,z):
    '''
    Set lamp function
    This function set the parameters to create the lights for
    the video
    
    Args: 
        scene:
            bpy.context.scene, contains the scene of the video
        x:
            float, x coordinate of the position of the lamp
        y:
            float, y coordinate of the position of the lamp
        z:
            float, z coordinate of the position of the lamp
        
    Returns:
        nothing is returned
    
    Raises:
        nothing is raised
    
    '''
    # Turn off the camera
    scene.camera = None  
    scene = bpy.context.scene
    # Create type of lamp (SUN to cover all area)
    lamp_data = bpy.data.lamps.new(name="lamp", type='SUN')  
    lamp_object = bpy.data.objects.new(name="Lamp", object_data=lamp_data)  
    scene.objects.link(lamp_object)
    # Set location of lamp  
    lamp_object.location = (x,y,z)  
    # Set rotation of lamp
    lamp_object.rotation_euler = (0,0,0)
    # Set specular to false to reduce time for rendering
    lamp_data.use_specular =False