import logging
import crossMemberClass
import historyCrossMemberClass
import historyMemberClass
import otherFunctions as others

logger = logging.getLogger('deformingLogging')

def deform(deformotion, decidor, elementTree, counter, ledByNormalMember, crossMembsList, validToCrossMembers, listLPs):
  if deformotion != 0.0 and decidor == len(elementTree[counter]):
    
    count = 0  #determines the loadpath the following member belongs to

    #Loop over all of the normal memebrs in the targeted tuple localtree[counter]
    for j in elementTree[counter]:
      
      #Deform the jth normal member of the targerted tuple localtree[counter] by an amount "defromotion"
      j.deform(deformotion)
          
      if j.calLength() == j.rigidLength:
        logger.debug("member {} has reached its maximum deformation length".format(j.name))
        if j.structural == True:
           for memb in listLPs.listOfLoadpaths[j.leftNode.loadpathLevel].listOfMembers:
             if memb.index == j.index:
               #turn this member off permenantly
               memb.changeState(False)
               #increase the number of turned off members in the corresponding loadpath
               listLPs.listOfLoadpaths[j.leftNode.loadpathLevel].increaseNoOffMembers()
               print("Number of Off Members equals to ", listLPs.listOfLoadpaths[j.leftNode.loadpathLevel].noOffMembers)
             else:
               memb.canDeform(True)
        else:  #here we know that this member was a gap, and we treat it in another way
          gapsHandeling.treatThisGap(j, listLPs)
            
      else: ##further improvement to this method is to introduce a list the contains the tuple of members that cant deform together due to the deformation of the current crossMember
        logger.debug("member {} has NOT reached its maximum deformation length".format(j.name))
        if ledByNormalMember == True:
          for memb in listLPs.listOfLoadpaths[j.leftNode.loadpathLevel].listOfMembers: #Switch all of the members along the loadpath containing member j off so they dont deform untill member j is done
             if memb.index == j.index:
               memb.canDeform(True)
             else:
               memb.canDeform(False)
        else:
          logger.debug("the procedure to deal with defomation led by crossMember has been called")
          for memb in listLPs.listOfLoadpaths[j.leftNode.loadpathLevel].listOfMembers:
            memb.canDeform(True)
                
      count = count + 1

    #this part of the function is to determine whether this carried out deformation is valid with respect to the list of cross members
      
    increment = 0
    for crossMemb in crossMembsList:
      crossMemb.checkNewCrossMembConfig()
      increment = increment + crossMemb.validToResume
    if increment == len(crossMembsList):
      validToCrossMembers = True

  return validToCrossMembers

          
