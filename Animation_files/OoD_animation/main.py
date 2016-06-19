import bpy   #Module for blender
import imp
import initialization
import setCamera
import setLamp
import Member
import LoadPath
import State
import MemberMassimo
import Structure

# Define main function
def main():
    imp.reload(initialization)   #Load library
    imp.reload(Member)
    imp.reload(LoadPath)
    imp.reload(State)
    imp.reload(MemberMassimo)
    imp.reload(Structure)
    
    #Delete everything
    initialization.initialize()
    initialization.delete_all()  #Clean everything
    
    objeto1 = MemberMassimo.hMember("e11",500, 1300, 500)
    objeto2 = MemberMassimo.hMember("e12",1300, 2100, 300)
    objeto3 = MemberMassimo.hMember("e31",200, 300, 0)
    objeto4 = MemberMassimo.hMember("e32",600, 1600, 0)
    objeto5 = MemberMassimo.hMember("e33",1800, 2100, 300)
    objeto6 = MemberMassimo.hMember("e41",200, 800, 500)
    objeto7 = MemberMassimo.hMember("e42",800, 1600, 400)
    objeto8 = MemberMassimo.hMember("e43",1600, 2100, 300)
    objeto9 = MemberMassimo.hMember("e51",800, 1600, 500)
    objeto10 = MemberMassimo.hMember("e52",1600, 2100, 300)
    input = [objeto1,objeto2,objeto3,objeto4,objeto5,objeto6,objeto7,objeto8,objeto9,objeto10]

    structure = Structure.Structure(input)
    
    #state1 = State.InitialState(listOfObjects)

main()
