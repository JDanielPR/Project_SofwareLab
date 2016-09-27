import member as mem
import loadpath as lp
import nextstep as ns
import node as n
import structure as struct
import itertools
import listOfLoadpaths
import crossMemberClass as cross

import time

#creating node objects
#ALL THESE STEPS ARE GOING TO BE CREATED IN THE FUNCTION "readXML" AND STORED 
#WITHIN A "structure" CLASS
#n11 = n.node(2)
#n12 = n.node(4)
#n13 = n.node(8)
#n14 = n.node(10)
#n21 = n.node(0)
#n22 = n.node(4)
#n23 = n.node(8)
#n24 = n.node(10)
#n31 = n.node(0)
#n32 = n.node(6)
#n33 = n.node(10)

#n11 = n.node(0)
#n12 = n.node(3)
#n13 = n.node(6)
#n14 = n.node(7)
#n15 = n.node(8)
#n21 = n.node(2)
#n22 = n.node(5)
#n23 = n.node(8)

#creating member objects
#ALL THESE STEPS ARE GOING TO BE CREATED IN THE FUNCTION "readXML" AND STORED 
#WITHIN A "structure" CLASS
#m1 = mem.member(n11,n12,0.50,'L1E1',None)
#m2 = mem.member(n12,n13,0.75,'L1E2',m1)
#m5 = mem.member(n13,n14,0.25,'L1E3',m2)
#m3 = mem.member(n21,n22,0.50,'L2E1',None)
#m4 = mem.member(n22,n23,0.75,'L2E2',m3)
#m6 = mem.member(n23,n24,0.50,'L2E3',m4)
#m7 = mem.member(n31,n32,0.50,'L3E1',None)
#m8 = mem.member(n32,n33,0.50,'L3E2',m7)

#m1 = mem.member(n11,n12,1,'L1E1',None,1)
#m2 = mem.member(n12,n13,1,'L1E2',m1,1)
#m3 = mem.member(n14,n15,1,'L1E3',m2,1)
#m4 = mem.member(n21,n22,1,'L2E1',None,2)
#m5 = mem.member(n22,n23,1,'L2E2',m4,2)

#organizing member objects in a single array
#ALL THESE STEPS ARE GOING TO BE CREATED IN THE FUNCTION "readXML" AND STORED 
#WITHIN A "structure" CLASS
#lp1 = lp.loadpath(1)
#lp2 = lp.loadpath(2)
#lp3 = lp.loadpath(3)

#lp1.addMember(m1)
#lp1.addMember(m2)
#lp1.addMember(m5)
#lp2.addMember(m3)
#lp2.addMember(m4)
#lp2.addMember(m6)
#lp3.addMember(m7)
#lp3.addMember(m8)

#lp1.addMember(m1)
#lp1.addMember(m2)
#lp1.addMember(m3)
#lp2.addMember(m4)
#lp2.addMember(m5)


#listLPs = listOfLoadpaths.listOfLoadpaths()
#listLPs.addLoadpath(lp1)
#listLPs.addLoadpath(lp2)
#listLPs.addLoadpath(lp3)

#creation of the structure in a single entity
#ALL THESE STEPS ARE GOING TO BE CREATED IN THE FUNCTION "readXML" AND STORED 
#WITHIN A "structure" CLASS
#givenStructure = struct.structure(listLPs)

#visualization of the given strucutre (NICHT WICHTIG)
#for i in givenStructure.listLoadpaths.listOfLoadpaths:
  #for j in i.listOfMembers:
    #print(j.calLength())
  #  print(j.leftNode.position,"",j.rightNode.position)

#solve the givenStructure
#givenStructure.solve()
'''

##test structure with cross member
#NODES
n1 = n.node(0)
n2 = n.node(4)
n3 = n.node(8)
n4 = n.node(12)
n5 = n.node(16)
n6 = n.node(20)

n7 = n.node(0)
n8 = n.node(4)
n9 = n.node(8)
n10 = n.node(12)
n11 = n.node(16)
n12 = n.node(20)

#MEMBERS
m1 = mem.member(n1,n2,0.75,'e1',None,0)
m2 = mem.member(n2,n3,0.75,'e2',m1,0)
m3 = mem.member(n3,n4,0.75,'e3',m2,0)
m4 = mem.member(n4,n5,0.75,'e4',m3,0)
m5 = mem.member(n5,n6,0.75,'e5',m4,0)

m6 = mem.member(n7,n8,0.75,'e6',None,1)
m7 = mem.member(n8,n9,0.75,'e7',m6,1)
m8 = mem.member(n9,n10,0.75,'e8',m7,1)
m9 = mem.member(n10,n11,0.75,'e9',m8,1)
m10 = mem.member(n11,n12,0.75,'e10',m9,1)

#LOADPATHS
lp1 = lp.loadpath(1)
lp2 = lp.loadpath(2)

lp1.addMember(m1)
lp1.addMember(m2)
lp1.addMember(m3)
lp1.addMember(m4)
lp1.addMember(m5)
lp2.addMember(m6)
lp2.addMember(m7)
lp2.addMember(m8)
lp2.addMember(m9)
lp2.addMember(m10)

listLPs = listOfLoadpaths.listOfLoadpaths()
listLPs.addLoadpath(lp1)
listLPs.addLoadpath(lp2)

#CROSS MEMBERS
cross1 = cross.crossMember(n3,n10,2)

crossList = [cross1]

'''
#MASSIMO's BENCHMARK TEST
#nodes
n1 = n.node(0)
n2 = n.node(4)
n3 = n.node(6)
n4 = n.node(0)
n5 = n.node(2)
n6 = n.node(6)
#members
m1 = mem.member(n1,n2,0.75,'e1',None,0)
m2 = mem.member(n2,n3,0.0,'e2',m1,0)
m3 = mem.member(n4,n5,0.0,'e3',None,1)
m4 = mem.member(n5,n6,0.75,'e4',m3,1)
#loadpaths
lp1 = lp.loadpath(1)
lp2 = lp.loadpath(2)
lp1.addMember(m1)
lp1.addMember(m2)
lp2.addMember(m3)
lp2.addMember(m4)
#list of loadpaths
listLPs = listOfLoadpaths.listOfLoadpaths()
listLPs.addLoadpath(lp1)
listLPs.addLoadpath(lp2)
#cross member
cross1 = cross.crossMember(n2,n5,0)
crossList = [cross1]
givenStructure = struct.structure(listLPs,crossList)
givenStructure.solve()
'''

#STRUCTURE
givenStructure = struct.structure(listLPs,crossList)

for i in givenStructure.listLoadpaths.listOfLoadpaths:
  for j in i.listOfMembers:
    print(j.calLength())
    print(j.leftNode.position,"",j.rightNode.position)

timeStart = time.time()
#solve the givenStructure
givenStructure.solve()

print("The time taken to solve this structure is ",(time.time() - timeStart))
'''
