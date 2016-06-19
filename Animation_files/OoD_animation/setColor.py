import bpy

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
    
def makeColor(name, diffuse, specular, alpha):
    color = bpy.data.materials.new(name)
    color.diffuse_color = diffuse
    color.diffuse_shader = 'LAMBERT' 
    color.diffuse_intensity = 1.0 
    color.specular_color = specular
    color.specular_shader = 'COOKTORR'
    color.specular_intensity = 0.5
    color.alpha = alpha
    color.ambient = 1
    return color

#Define colors
red = makeColor('Red', (1,0,0), (1,1,1), 1)
blue = makeColor('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
black = makeColor('Black', (0,0,0), (2.5,1.5,1), 0.5) 
white = makeColor('White', (1,1,1), (2.5,1.5,1), 0.5) 
green = makeColor('Green', (0,1,0), (2.5,1.5,1), 0.5) 
