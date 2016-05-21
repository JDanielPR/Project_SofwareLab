'''
Created on 25/03/2016

@author: Admin
'''
import bpy   #Module for blender
import math
import imp
import random
from bpy import context
from mathutils import Vector
from math import pi
from operator import itemgetter # to use max
import myHeader
import colores
import mathutils
import Node
import Element
import Structure
import Wall

# Define main function
def main():
    print("The program starts here")
    imp.reload(myHeader)   #Load library
    imp.reload(Node)       #Load library
    imp.reload(Element)    #Load library
    imp.reload(Structure)  #Load library
    imp.reload(Wall)       #Load library
    #imp.reload(Structure)  #Load library
    myHeader.delete_all()  #Clean everything

    # Define the list of nodes and member
    (nodes,members, numberOfNodes, numberOfMembers, numberOfPaths) = myHeader.leerTxt()   
    my_nodes = []     #Define nodes list
    my_elements = []  #Define memberslist
    my_structure  = Structure.Structure(nodes,members, numberOfNodes, numberOfMembers, numberOfPaths) 

    # Definition of variables
    cursor = context.scene.cursor_location            #Set the cursor location
    start_pos = (0,0,0)                               #Define the first positiom

    my_Wall = Wall.Wall(my_structure.get_coordinateOfTheVeryFirstNode())
    my_Wall.get_wall()
    # Set animation start and stop
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = 10 + 50 + my_structure.get_timeOfTheAnimation()/10 
    
#Delete everything
myHeader.initialize()
#Call the main function
main()
#Start animation
#bpy.ops.screen.animation_play(reverse=False, sync=False) 

