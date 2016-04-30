'''
Created on 08/04/2016

@author: Admin
'''
import bpy

#Define colors
def initcolors(r,g,b):
    global color
    color= bpy.data.materials.new("color")
    color.diffuse_color = (r/255.0, g/255.0 , b/255.0) # r , g , b
    return color

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat

    