import logging
import CrossComponent
import HistoryCrossComponent
import HistoryComponent
import OtherFunctions
import GapsHandeling

logger = logging.getLogger('deform')

def deform(
  deformationAmount,
  decidor,
  branch,
  ledByComponent,
  listCrossComponents,
  validToCrossComponents,
  listLoadpaths):
  '''Function that perform the deformation and return its validity to cross components

  This function does the deformation upon the components inside the branch of
  possibilities. In addition, it changes some key attributes of involved 
  components as a result of the deformation step and chooses the right way of
  doing this. For example, the kind of component as being structural or gap has
  different procedures, and also the kind of driving component such as a normal
  component or cross component has different procedures
  '''

  # Insuring that deformation will not be carried out if the deformation step
  # amount was zero
  if deformationAmount != 0.0:

    # Loop over all of the involved components in the possibilities branch
    for component in branch:

      # Perform the deformation upon the component
      component.deform(deformationAmount)
      print("component current length is ", component.calc_length())

      # If the component has reached its deformation limit, perfrom this
      if component.calc_length() == component.rigidLength:
        
        logger.debug(
          "Component {} has reached its maximum deformation length".format(
            component.name
            )
          )

        # if the component is structural and not a gap, perfrom this 
        if component.isStructural == True:

          # This is the loadpath level the component belongs to
          loadpathLevel = component.leftNode.loadpathLevel

          # Loop over all the other components within the deforming component's
          # own loadpath 
          for otherComponent in listLoadpaths[loadpathLevel].listComponents:
             
            if otherComponent.componentIndex == component.componentIndex:
              print(otherComponent.name)
              # Switch the deforming component's perminantlyBlockedDeformation
              # to False, the component is no longer able to deform
              component.change_perminantlyBlockedDeformation(False)
              
              # Increase the number of components that are unable to deform
              # anymore in the deforming component's own loadpath
              listLoadpaths[
                component.leftNode.loadpathLevel
                ].increase_noComponentsNotDeformable()
              
              print("Number of Off Members equals to ", listLoadpaths[component.leftNode.loadpathLevel].noComponentsNotDeformable)
            else:
              # For all of the other components within the deforming component's
              # own loadpath, switch their attribute temporarilyBlockedDeformation
              # to True
              otherComponent.change_temporarilyBlockedDeformation(True)

        # If the deforming component is a gap, then perform this      
        else:  
          GapsHandeling.treat_this_gap(component, listLoadpaths)

      # If the deforming component has not reached its deformation limit, then
      # perform this
      else:
        logger.debug(
          "member {} has NOT reached its maximum deformation length".format(
            component.name
            )
          )
        # If the deformation amount was determined by a normal component, then
        # perfrom this
        if ledByComponent == True:
          print("loadpath level is: ",component.leftNode.loadpathLevel)
          # Loop over all of the components within the deforming component's own
          # loadpath
          for otherComponent in listLoadpaths[
            component.leftNode.loadpathLevel].listComponents:

            # Switch the deforming component's attribute
            # temporarilyBlockedDeformation to True
             if otherComponent.componentIndex == component.componentIndex:
               otherComponent.change_temporarilyBlockedDeformation(True)
             # Switch all of the other components' attribute
             # temporarilyBlockedDeformation to False
             else:
               otherComponent.change_temporarilyBlockedDeformation(False)

        # If the deformation amount was determined by a cross component, then
        # perfrom this
        else:
          logger.debug("dealing with defomation led by cross-Components is activated")
          for otherComponent in listLoadpaths[component.leftNode.loadpathLevel].listComponents:
            otherComponent.change_temporarilyBlockedDeformation(True)

    # This part of the function determines whether this carried out deformation
    # step is valid to all the cross components
    increment = 0
    # Loop over all of the cross components
    for crossComponent in listCrossComponents:
      # Check the validity of the deformation step for the cross component
      crossComponent.check_new_cross_component_config()
      # increment this counter if the deformation step was valid
      increment = increment + crossComponent.deformationStepIsValid
    
    # If the "increment" counter has incremented by all of the cross component
    # then its value should be equal to the number of cross components and that
    # means that deformation step is valid to cross components
    if increment == len(listCrossComponents):
      validToCrossComponents = True
    else:
      validToCrossComponents = False

    
  return validToCrossComponents

          
