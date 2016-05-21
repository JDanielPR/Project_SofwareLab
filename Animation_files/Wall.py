import imp
import math
import bpy   #Module for blender

class Wall():
    def __init__(self , positionOfTheWall):
        self.positionOfTheWall = positionOfTheWall
    def get_wall(self):
        # Create wall
        bpy.ops.mesh.primitive_cube_add(location = (self.positionOfTheWall - 1000,0,0), rotation=(0,0,math.radians(90)))
        bpy.context.object.dimensions = 3000, 1000, 100
        bpy.ops.object.shade_smooth() 
        w = bpy.context.object
        w.name = "Wall"
        # Select wall
        bpy.context.scene.objects.active = bpy.data.objects["Wall"]
        bpy.data.objects['Wall'].select = True  
        bpy.ops.object.select_all(action = 'TOGGLE')