import historyMemberClass as historyMember
import historyCrossMemberClass as historyCrossMember
import logging 

logger = logging.getLogger('otherFunctions')

'''
FILE DESCRIBTION:
This file groups all of the functions that are used some where in the implementation of the OoD solver
'''

#This function assigns indexes to the members with respect to their position in their corresponding loadpaths
def indexor(listLPs):
  for i in listLPs.listOfLoadpaths:
    x = 0
    for j in i.listOfMembers:
      j.index = x
      x += 1

#This function restores the previous state to a list of members at the same loadpath
def restoreMembersConfig(listMembers):
  for member in listMembers:
    x = len(member.history)
    logger.debug("Member {} is restoring their previous states".format(member.name))
    member.leftNode.position = member.history[x-1].leftNodePosition
#    member.dLength = member.history[x-1].dLength
    member.state = member.history[x-1].state
    member.deformPossibility = member.history[x-1].deformPossibility
    print("Now, member",member.name,"has state ",member.state)
    member.history.remove(member.history[x-1])
    leftMemb = member.leftMember
    while leftMemb != None:
      x = len(leftMemb.history)
      logger.debug("Member {} is restoring its previous states".format(leftMemb.name)) 
      leftMemb.leftNode.position = leftMemb.history[x-1].leftNodePosition
#      leftMemb.dLength = leftMemb.history[x-1].dLength
      leftMemb.state = leftMemb.history[x-1].state
      leftMemb.deformPossibility = leftMemb.history[x-1].deformPossibility
      print("Now, member",leftMemb.name,"has state ",leftMemb.state)
      leftMemb.history.remove(leftMemb.history[x-1])
      leftMemb = leftMemb.leftMember
  
def storeMembersConfig(listMembers):
  for member in listMembers:
    logger.debug("parameters of the member {} are being stored as a history".format(member.name))
    historyElement = historyMember.historyMember(member.leftNode.position , member.state , member.deformPossibility)
    member.history.append(historyElement)
    print("member",member.name," history is")
    for i in member.history:
      print("state: ",i.state)

def restoreCrossMembersConfig(listCrossMembers):
  logger.debug("Cross members are restoring their previous states")
  for crossMember in listCrossMembers:
    x = len(crossMember.history)
    crossMember.horizDefLength = crossMember.history[x-1].defLength
    crossMember.noContNoElong = crossMember.history[x-1].noContNoElong
    crossMember.validToResume = crossMember.history[x-1].validToResume
    crossMember.failureCausingCrossMember = crossMember.history[x-1].failureCausingCrossMember
    crossMember.history.remove(crossMember.history[x-1])

def storeCrossMembersConfig(listCrossMembers):
  logger.debug("parameters of cross members are being stored as a history")
  for crossMember in listCrossMembers:
    historyElement = historyCrossMember.historyCrossMember(crossMember.horizDefLength , crossMember.NoContNoElong , crossMember.validToResume , crossMember.failureCausingCrossMember)
    crossMember.history.append(historyElement)

#this function enable us to restore the state of the member before the current defromation step along with the rest of the left members
def restoreMembers(listMembers):
  logger.debug("Members are restoring...")
  restoreMembersConfig(listMembers)

def restoreCrossMembers(crossMembersList):
  logger.debug("Cross members are restoring...")
  restoreCrossMembersConfig(crossMembersList)

def restore(elementTree,counter,listLoadpaths,listCrossMembers):
  for member in elementTree[counter]:
    x = len(member.history)
    print(member.name)
    print("the value of x is: ",x)
    if member.state != member.history[x - 1].state:
      listLoadpaths.listOfLoadpaths[member.leftNode.loadpathLevel].decreaseNoOffMembers()
  restoreMembers(elementTree[counter])
  restoreCrossMembers(listCrossMembers)
