import math  #Module for math operations
import bpy   #Module for blender
import imp
import setColor
import Node
import BlenderMesh

imp.reload(setColor)         #Load library
imp.reload(Node)             #Load library
imp.reload(BlenderMesh)    #Load library
        

class Puntos():
    def __init__(self , numberOfNode , cx, cy):
        self.numberOfNode = numberOfNode             # Every element has a unique number
        self.cx = cx                                # First object node
        self.cy = cy                                # Second object node

        oE = BlenderMesh.BlenderNode(str(self.numberOfNode), (self.cx, self.cy, 0),(0, math.radians(90) ,math.pi/4))
        self.blenderElement = oE.get_geometricalObject()
        selectedObject = bpy.context.selected_objects
        setColor.setMaterial(bpy.context.object, setColor.black) # Elements in black are rigid elements
        bpy.ops.object.shade_smooth() 
        
    def get_blenderElement(self):
        return self.blenderElement   