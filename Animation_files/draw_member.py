import bpy
import mathutils
import math

# define some colors as global constants
RED = bpy.data.materials.new("RED")
RED.diffuse_color = (1.0, 0.0, 0.0)

BLACK = bpy.data.materials.new("BLACK")
BLACK.diffuse_color = (0.0, 0.0, 0.0)

WHITE = bpy.data.materials.new("WHITE")
WHITE.diffuse_color = (1.0, 1.0, 1.0)

# trying to draw a single member with 2 nodes, a rigid and a deformable part

# e====-------------e
# | |       |       |
# | |       |       node
# | |       |       
# | |   deformable part
# | |
# | rigid part
# |
# node

x_start = 0
x_middle = 1
x_end = 5
y = 0
z = 0

h = 0.1


def node_vertices(x, y, z, h):
    return [
        mathutils.Vector((x + h, y + h, z)),
        mathutils.Vector((x - h, y + h, z)),
        mathutils.Vector((x - h, y - h, z)),
        mathutils.Vector((x + h, y - h, z))
        ]
        
def rigid_rectangle_vertices(x_start, x_middle, y, z, h):
    return [
        mathutils.Vector((x_start + h, y + h, z)),
        mathutils.Vector((x_middle, y + h, z)),
        mathutils.Vector((x_middle, y - h, z)),
        mathutils.Vector((x_start + h, y - h, z))
        ]
def deformable_rectangle_vertices(x_middle, x_end, y, z, h):
    return [
        mathutils.Vector((x_end - h, y + h, z)),
        mathutils.Vector((x_middle, y + h, z)),
        mathutils.Vector((x_middle, y - h, z)),
        mathutils.Vector((x_end -h, y - h, z))
        ]

# draw node
StartNodeMesh = bpy.data.meshes.new("Start_node")
StartNodeMesh.from_pydata \
                          (
                              node_vertices(x_start, y, z, h),
                              [ ],
                              [ [0, 1, 2, 3] ]
                            )
StartNodeMesh.update()
StartNodeObj = bpy.data.objects.new("Start_node", StartNodeMesh)
StartNodeObj.active_material = RED
bpy.context.scene.objects.link(StartNodeObj)


# draw rigid part
RigidPartMesh = bpy.data.meshes.new("Rigid_part")
RigidPartMesh.from_pydata \
                          (
                              rigid_rectangle_vertices \
                              ( 
                                x_start,
                                x_middle,
                                y,
                                z,
                                h
                              ),
                              [ ],
                              [ [0, 1, 2, 3] ]
                            )
RigidPartMesh.update()
RigidPartObj = bpy.data.objects.new("Rigid_part", RigidPartMesh)
RigidPartObj.active_material = BLACK
bpy.context.scene.objects.link(RigidPartObj)

# draw deformable part
DeformablePartMesh = bpy.data.meshes.new("Deformable_part")
DeformablePartMesh.from_pydata \
                          (
                              deformable_rectangle_vertices \
                              ( 
                                x_middle,
                                x_end,
                                y,
                                z,
                                h
                              ),
                              [ ],
                              [ [0, 1, 2, 3] ]
                            )
DeformablePartMesh.update()
DeformablePartObj = bpy.data.objects.new("Deformable_part", DeformablePartMesh)
DeformablePartObj.active_material = WHITE
bpy.context.scene.objects.link(DeformablePartObj)

# draw node
EndNodeMesh = bpy.data.meshes.new("End_node")
EndNodeMesh.from_pydata \
                          (
                              node_vertices(x_end, y, z, h),
                              [ ],
                              [ [0, 1, 2, 3] ]
                            )
EndNodeMesh.update()
EndNodeObj = bpy.data.objects.new("End_node", EndNodeMesh)
EndNodeObj.active_material = RED
bpy.context.scene.objects.link(EndNodeObj)
