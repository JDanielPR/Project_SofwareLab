'''
Created on 25/03/2016

@author: Admin
'''
import bpy   #Module for blender
import math
import myHeader
import colores
import imp
from bpy import context

#Set the active layers
bpy.context.scene.layers[0] = True
bpy.context.scene.layers[0] = False


#Define the main function
def main():
    delete_all()    #Clean everything
    imp.reload(colores)
    imp.reload(myHeader)
    
    (nodes,tubes, numberNodes, numberTubes) = myHeader.leerTxt()
    my_nodes = []
    for i in range(numberNodes):
        my_nodes.append(myHeader.Node(i+1, nodes[i][0],nodes[i][1],nodes[i][2]))
        my_tubes = []
    for i in range(numberTubes):
        my_tubes.append(myHeader.Tube(i+1,my_nodes[int(tubes[i][0])-1],my_nodes[int(tubes[i][1])-1],tubes[i][2]))
    print (my_tubes[5].get_A())
    print (my_tubes[5].get_B())
    print (my_tubes[5].calcLength())
    print (my_tubes[5].calcB())
    pipeNetwork = myHeader.PipeNet(my_nodes,my_tubes)
    print (pipeNetwork.calcFlux())
    
    #Define variables for primitive shapes
    cubeobject = bpy.ops.mesh.primitive_cube_add
    sphereobject = bpy.ops.mesh.primitive_uv_sphere_add
    cylinderobject = bpy.ops.mesh.primitive_cylinder_add

    #Define variables
    cursor = context.scene.cursor_location  #Set the cursor location
    start_pos = (0,0,0)  #Define the first position

    x = 0.0
    y = 0.0
    z = 0.0

    for i in range(numberTubes):
        #cubeobject(location = (x ,y, z))
        inx1 = my_tubes[i].get_A() - 1
        iny1 = my_tubes[i].get_A() - 1
        inx2 = my_tubes[i].get_B() - 1
        iny2 = my_tubes[i].get_B() - 1
        
        xi = (my_nodes[inx1].get_x()  ) / 100
        yi = (my_nodes[iny1].get_y()) / 100
        xj = (my_nodes[inx2].get_x()  ) / 100
        yj = (my_nodes[iny2].get_y()) / 100
        print( xi , " ", yi, "  ", xj , " ", yj)
        a1 = math.asin(((yj-yi)/(my_tubes[i].calcLength() / 100)))
        a2 = math.radians(90)
        a3 = 0
        
        if xi == xj:
            x = xi
        else:
            x = math.fabs(xj - xi)*0.5 + xi
        if yi == yj:
            y = yi
        else:
            y = (yj - yi)*0.5 + yi
        z = 0.0
        
        #print(x)
        
        cylinderobject(
                       radius = my_tubes[i].get_d()/2, 
                       depth = my_tubes[i].calcLength() / 100,
                       location = (x, y, z),
                       rotation = (a1, a2, a3)  ) 
        y+=10
        #bpy.ops.transform.resize(value = (2 ,20, 2)) #for cube
        #Get the active object and assign it a color
        getactiveobject = bpy.context.selected_objects[0]
        getactiveobject.active_material = colores.initcolors(138.0, 255.0, 0.0)
    
def delete_all():
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.select_all(action = 'TOGGLE')
    bpy.ops.object.delete(use_global = False)
 
#Call the main function   
main()
