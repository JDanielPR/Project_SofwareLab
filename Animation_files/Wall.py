import imp
import math
import bpy   #Module for blender
import setColor
import BlenderMesh

imp.reload(setColor)       #Load library
imp.reload(BlenderMesh)    #Load library

class Wall():
    def __init__(self , positionOfTheWallX, positionOfTheWallY ,height):
        self.positionOfTheWallX = positionOfTheWallX
        self.positionOfTheWallY = positionOfTheWallY
        self.height = height
        self.w = []
        
    def build_wall(self):
        # Create wall
        oW = BlenderMesh.BlenderWall(str(1), (self.positionOfTheWallX - 1000, self.positionOfTheWallY + self.height/2, 0), self.height,(0,0,math.radians(90)))
        self.w = oW.get_geometricalObject()
        selectedObject = bpy.context.selected_objects
        bpy.ops.object.shade_smooth() 
        setColor.setMaterial(self.w, setColor.blue)
        # Select wall
        bpy.context.scene.objects.active = bpy.data.objects["Wall1"]
        bpy.data.objects['Wall1'].select = True  
        bpy.ops.object.select_all(action = 'TOGGLE')
