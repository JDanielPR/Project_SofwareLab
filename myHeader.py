'''
Created on 06/04/2016

@author: Admin
'''
import math


def leerTxt():
    print ("Herzlich willkommen")
    file = open("C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\pipedata.txt", "r") 
    
    numberNodes = 0
    numberTubes = 0
    numberNodes = int(file.readline())
    numberTubes = int(file.readline())

    i = 0
    j = 0
  
    arreglo = []
    nodes = []
    tubes = []
    arreglo = file.read().split()
    file.close()
    
    for i in range( numberNodes + numberTubes):
        if i < numberNodes:
            nodes.append([])
        else:
            tubes.append([])
            
        for j in range(4*(i+1)-4,4*(i+1)):
            if i < numberNodes:
                nodes[i].append(float(arreglo[j]))
            else:
                tubes[i - numberNodes].append(float(arreglo[j]))
    
    return (nodes, tubes , numberNodes, numberTubes)

class Node():
    def __init__(self , num = 0 , cx = 0.0 , cy = 0.0 , Q = 0.0):
        self.num = num
        self.cx = cx
        self.cy = cy
        self.Q = Q
    def get_num(self):
        return self.num
    def get_x(self):
        return self.cx
    def get_y(self):
        return self.cy
    def get_Q(self):
        return self.Q
        
class Tube():
    q = 0
    def __init__(self , num  , nodeA , nodeB  , d, up):
        self.num = num
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.d = d
        self.up = up
    def get_num(self):
        return self.num
    def get_A(self):
        return self.nodeA.get_num()
    def get_B(self):
        return self.nodeB.get_num()
    def get_d(self):
        return self.d
    def get_q(self):
        return self.q
    def get_up(self):
        return self.up
    def calcLength(self):
        return math.sqrt((self.nodeA.get_x() - self.nodeB.get_x()) ** 2 + (self.nodeA.get_y() - self.nodeB.get_y()) ** 2)
    
    
class PipeNet():
    def __init__(self , vector_nodes, vector_tubes):
        self.vector_nodes = vector_nodes
        self.vector_tubes = vector_tubes

    
