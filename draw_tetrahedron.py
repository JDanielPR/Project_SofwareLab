import bpy
import mathutils
import math
Vertices = \
          [
            mathutils.Vector((0, -1 / math.sqrt(3),0)),
            mathutils.Vector((0.5, 1 / (2 * math.sqrt(3)), 0)),
            mathutils.Vector((-0.5, 1 / (2 * math.sqrt(3)), 0)),
            mathutils.Vector((0, 0, math.sqrt(2 / 3))),
          ]
NewMesh = bpy.data.meshes.new("Tetrahedron")
NewMesh.from_pydata \
          (
            Vertices,
            [],
            [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
          )
NewMesh.update()
NewObj = bpy.data.objects.new("Tetrahedron", NewMesh)
bpy.context.scene.objects.link(NewObj)