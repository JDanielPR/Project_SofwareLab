import component as c
import deformation_step as d

def fake_solver():
    i_s = list()
    d_h = dict()

    # fake system:
    #    e1    e2   e3
    #  o--xo o--xo---xxxo
    #         c1/
    #      e4  /  e5       e6
    #    o---xo----xxo   o---xo
    #
    e1 = c.Component("e1",  25,  50, 10, 1, 1, 35)
    e2 = c.Component("e2",  75, 110, 15, 1, 1, 90)
    e3 = c.Component("e3", 110, 160, 25, 1, 1, 120)

    e4 = c.Component("e4",  50,  90, 15, 2, 2)
    e5 = c.Component("e5",  90, 130, 20, 2, 2)
    e6 = c.Component("e6", 150, 190, 15, 2, 2, 140)

    c1 = c.Component("c1",  90, 110, 10, 2, 1)

    i_s.append(e1)
    i_s.append(e2)
    i_s.append(e3)
    i_s.append(e4)
    i_s.append(e5)
    i_s.append(e6)
    i_s.append(c1)

    
    d_h[e1] = list()
    d_h[e2] = list()
    d_h[e3] = list()
    d_h[e4] = list()
    d_h[e5] = list()
    d_h[e6] = list()
    d_h[c1] = list()

    d_h[e1].append(d.DeformationStep(25, 0, "m"))
    d_h[e2].append(d.DeformationStep(25, 0, "m"))
    d_h[e3].append(d.DeformationStep(25, 0, "m"))
    d_h[e4].append(d.DeformationStep(25, 0, "m"))
    d_h[e5].append(d.DeformationStep(25, 0, "m"))
    d_h[e6].append(d.DeformationStep(25, 0, "m"))
    d_h[c1].append(d.DeformationStep(25, 0, "m"))

    d_h[e2].append(d.DeformationStep(25, 25, "m"))
    d_h[e3].append(d.DeformationStep(25, 25, "m"))
    d_h[e4].append(d.DeformationStep(25, 25, "m"))
    d_h[e5].append(d.DeformationStep(25, 25, "m"))
    d_h[e6].append(d.DeformationStep(25, 25, "m"))
    d_h[c1].append(d.DeformationStep(25, 25, "m"))    

    d_h[e2].append(d.DeformationStep(15, 50, "d"))
    d_h[e3].append(d.DeformationStep(15, 50, "m"))
    d_h[e4].append(d.DeformationStep(15, 50, "d"))
    d_h[e5].append(d.DeformationStep(15, 50, "m"))
    d_h[e6].append(d.DeformationStep(15, 50, "m"))
    d_h[c1].append(d.DeformationStep(15, 50, "m"))

    d_h[e1].append(d.DeformationStep(10, 65, "d"))
    d_h[e2].append(d.DeformationStep(10, 65, "m"))
    d_h[e3].append(d.DeformationStep(10, 65, "m"))
    d_h[e6].append(d.DeformationStep(10, 65, "m"))
    d_h[c1].append(d.DeformationStep(10, 65, "d"))

    d_h[e3].append(d.DeformationStep(10, 75, "d"))
    d_h[e6].append(d.DeformationStep(10, 75, "m"))
    
    d_h[e3].append(d.DeformationStep(15, 85, "d"))
    d_h[e6].append(d.DeformationStep(15, 85, "d"))

    d_h[e5].append(d.DeformationStep(20, 100, "d"))
    d_h[e6].append(d.DeformationStep(20, 100, "m"))
        
    return i_s, [d_h, d_h]
