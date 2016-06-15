import member as mem
import loadpath as lp
import nextstep as ns
import node as n
import itertools

#creating node objects
n11 = n.node(0)
n12 = n.node(4)
n13 = n.node(8)
n14 = n.node(10)
n21 = n.node(0)
n22 = n.node(4)
n23 = n.node(8)
n24 = n.node(10)
n31 = n.node(0)
n32 = n.node(6)
n33 = n.node(10)

#creating member objects (THIS CAN BE DONE AUTOMATICALLY)
m1 = mem.member(n11,n12,0.50,'L1E1',None)
m2 = mem.member(n12,n13,0.75,'L1E2',m1)
m5 = mem.member(n13,n14,0.25,'L1E3',m2)
m3 = mem.member(n21,n22,0.50,'L2E1',None)
m4 = mem.member(n22,n23,0.75,'L2E2',m3)
m6 = mem.member(n23,n24,0.50,'L2E3',m4)
m7 = mem.member(n31,n32,0.50,'L3E1',None)
m8 = mem.member(n32,n33,0.50,'L3E2',m7)

#organizing member objects in a single array (THIS CAN BE DONE AUTOMATICALLY)
lp1 = lp.loadpath(1)
lp2 = lp.loadpath(2)
lp3 = lp.loadpath(3)

lp1.addMember(m1)
lp1.addMember(m2)
lp1.addMember(m5)
lp2.addMember(m3)
lp2.addMember(m4)
lp2.addMember(m6)
lp3.addMember(m7)
lp3.addMember(m8)

loadpath = [[m1,m2,m5],[m3,m4,m6],[m7,m8]]

for i in loadpath:
  for j in i:
    print(j.calLength())
    print(j.leftNode.position,"",j.rightNode.position)

#create the tree of possibilities 
lpgroup = list(itertools.product(*loadpath))

#prints the motion possibilities
for i in lpgroup:
  for j in i:
    print(j.name)
print('\n')

nstep = ns.nextstep(lpgroup,None,None)

##ANOTHER STRUCTURE FOR THE TEST OF MEMBERS WITH GAPS
#m1 = mem.member(0,3,1.00,'GAP1',None)
#m2 = mem.member(3,7,0.75,'L1E1',m1)
#m3 = mem.member(7,11,0.25,'GAP2',m2)
#m4 = mem.member(11,13,0.50,'L1E3',m3)

#m5



  

  


