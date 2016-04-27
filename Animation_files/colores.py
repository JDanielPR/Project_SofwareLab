'''
Created on 08/04/2016

@author: Admin
'''
import bpy

#Define the colors
def initcolors(r,g,b):
    
    global color
    color= bpy.data.materials.new("color")
    color.diffuse_color = (r/255.0, g/255.0 , b/255.0) # r , g , b
    
    return color
    '''#Create a new REDfor the object
    global redcolor
    redcolor= bpy.data.materials.new("red")
    redcolor.diffuse_color = (1.0, 0.0 , 0.0) # r , g , b
    
    #Create a new GREEN for the object
    global greencolor
    greencolor= bpy.data.materials.new("green")
    greencolor.diffuse_color = (0.0, 1.0 , 0.0) # r , g , b
    
    #Create a new BLUE for the object
    global bluecolor
    bluecolor= bpy.data.materials.new("blue")
    bluecolor.diffuse_color = (0.0, 0.0 , 1.0) # r , g , b
    
    #Create a new CYAN for the object
    global cyancolor
    cyancolor= bpy.data.materials.new("cyan")
    cyancolor.diffuse_color = (0.0, 1.0 , 1.0) # r , g , b
    
    #Create a new MAGENTA for the object
    global magentacolor
    magentacolor= bpy.data.materials.new("magenta")
    magentacolor.diffuse_color = (1.0, 0.0 , 1.0) # r , g , b
    
    #Create a new YELLOW for the object
    global yellowcolor
    yellowcolor= bpy.data.materials.new("yellow")
    yellowcolor.diffuse_color = (1.0, 1.0 , 0.0) # r , g , b
    
    #Create a new BLACK for the object
    global blackcolor
    blackcolor= bpy.data.materials.new("black")
    blackcolor.diffuse_color = (0.0, 0.0 , 0.0) # r , g , b
    
    #Create a new BLACK for the object
    global silvercolor
    silvercolor= bpy.data.materials.new("silver")
    silvercolor.diffuse_color = (1, 1 , 1) # r , g , b'''
    