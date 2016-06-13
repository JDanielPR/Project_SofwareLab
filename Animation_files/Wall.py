import imp
import math
import bpy   #Module for blender

class Wall():
    def __init__(self , positionOfTheWallX, positionOfTheWallY ,height):
        self.positionOfTheWallX = positionOfTheWallX
        self.positionOfTheWallY = positionOfTheWallY
        self.height = height
    def build_wall(self):
        # Create wall
        bpy.ops.mesh.primitive_cube_add(location = (self.positionOfTheWallX - 1000,self.positionOfTheWallY + self.height/2 ,0), rotation=(0,0,math.radians(90)))
        bpy.context.object.dimensions = self.height + 700, 1000, 100
        bpy.ops.object.shade_smooth() 
        w = bpy.context.object
        w.name = "Wall"
        # Select wall
        bpy.context.scene.objects.active = bpy.data.objects["Wall"]
        bpy.data.objects['Wall'].select = True  
        bpy.ops.object.select_all(action = 'TOGGLE')