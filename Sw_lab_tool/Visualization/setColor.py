import bpy

def setColor(ob, color):
    '''Set the color of an object
    
    Args:
        ob:
            blender object, the object to color
        color:
            color object, color
    
    Returns: 
        nothing is returned
    
    Raises:
        nothing is raised
    '''
    me = ob.data
    me.materials.append(color)

def makeColor(name, diffuse):
    '''Creates color
    
    Args:
        name:
            string, name of the color
        diffuse:
            value of difussion
    
    Returns: 
        new color
    
    Raises:
        nothing is raised
    '''
    color = bpy.data.materials.new(name)
    color.diffuse_color = diffuse
    color.diffuse_intensity = 1.0 
    color.specular_intensity = 0.5
    color.alpha = 0.5
    color.ambient = 1
    return color

#Define colors
red =   makeColor('Red',  (1,0,0))
blue =  makeColor('Blue', (0,0,1))
black = makeColor('Black',(0,0,0)) 
white = makeColor('White',(1,1,1)) 
green = makeColor('Green',(0,1,0)) 
gray =  makeColor('Gray', (0.6,0.6,0.6)) 
dark_gray =  makeColor('Gray', (0.2,0.2,0.2)) 


