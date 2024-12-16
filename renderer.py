# trace generated using paraview version 5.13.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *

def render(filename="output.60000.vts", output_file="test.png"):
    #### disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()

    # create a new 'XML Structured Grid Reader'
    output60000vts = XMLStructuredGridReader(registrationName=filename, FileName=[f'C:\\Users\\Gebruiker\\Desktop\\Visualization\\wildfire_svvr\\data\\raw\\{filename}'])

    # Properties modified on output60000vts
    output60000vts.PointArrayStatus = ['rhof_1', 'theta', 'u', 'v', 'w']
    output60000vts.TimeArray = 'None'

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    output60000vtsDisplay = Show(output60000vts, renderView1, 'StructuredGridRepresentation')

    # trace defaults for the display properties.
    output60000vtsDisplay.Representation = 'Outline'

    # reset view to fit data
    renderView1.ResetCamera(False, 0.9)

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Contour'
    contour1 = Contour(registrationName='Contour1', Input=output60000vts)

    # rename source object
    RenameSource('Fire', contour1)

    # Properties modified on contour1
    contour1.ContourBy = ['POINTS', 'theta']
    contour1.Isosurfaces = [400.0, 488.6494954427083, 577.2989908854166, 665.948486328125, 754.5979817708333, 843.2474772135416, 931.89697265625, 1020.5464680989583, 1109.1959635416665, 1197.845458984375]

    # show data in view
    contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    contour1Display.Representation = 'Surface'

    # show color bar/color legend
    contour1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # get color transfer function/color map for 'theta'
    thetaLUT = GetColorTransferFunction('theta')

    # get opacity transfer function/opacity map for 'theta'
    thetaPWF = GetOpacityTransferFunction('theta')

    # get 2D transfer function for 'theta'
    thetaTF2D = GetTransferFunction2D('theta')

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    thetaLUT.ApplyPreset('Yellow - Gray - Blue', True)

    # Properties modified on thetaLUT
    thetaLUT.EnableOpacityMapping = 0

    # Properties modified on thetaLUT
    thetaLUT.EnableOpacityMapping = 1

    # set active source
    SetActiveSource(output60000vts)

    # create a new 'Contour'
    contour1_1 = Contour(registrationName='Contour1', Input=output60000vts)

    # rename source object
    RenameSource('Smoke', contour1_1)

    # Properties modified on contour1_1
    contour1_1.ContourBy = ['POINTS', 'theta']
    contour1_1.Isosurfaces = [299.7328796386719, 310.87367078993054, 322.0144619411892, 333.15525309244794, 344.2960442437066, 355.43683539496527, 366.57762654622394, 377.71841769748266, 388.85920884874133, 400.0]

    # show data in view
    contour1_1Display = Show(contour1_1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    contour1_1Display.Representation = 'Surface'

    # show color bar/color legend
    contour1_1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # hide data in view
    Hide(contour1_1, renderView1)

    # set active source
    SetActiveSource(contour1_1)

    # show data in view
    contour1_1Display = Show(contour1_1, renderView1, 'GeometryRepresentation')

    # show color bar/color legend
    contour1_1Display.SetScalarBarVisibility(renderView1, True)

    # hide data in view
    Hide(contour1, renderView1)

    # set active source
    SetActiveSource(contour1)

    # show data in view
    contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

    # show color bar/color legend
    contour1Display.SetScalarBarVisibility(renderView1, True)

    # set active source
    SetActiveSource(contour1_1)

    # set active source
    SetActiveSource(output60000vts)

    # create a new 'Contour'
    contour1_2 = Contour(registrationName='Contour1', Input=output60000vts)

    # Properties modified on contour1_2
    contour1_2.ContourBy = ['POINTS', 'rhof_1']
    contour1_2.Isosurfaces = [0.0, 0.06666666931576198, 0.13333333863152397, 0.20000000794728595, 0.26666667726304794, 0.3333333465788099, 0.4000000158945719, 0.4666666852103339, 0.5333333545260959, 0.6000000238418579]

    # show data in view
    contour1_2Display = Show(contour1_2, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    contour1_2Display.Representation = 'Surface'

    # show color bar/color legend
    contour1_2Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # get color transfer function/color map for 'rhof_1'
    # rhof_1LUT = GetColorTransferFunction('rhof_1')

    # # Properties modified on rhof_1LUT
    # # rhof_1LUT.EnableOpacityMapping = 1
    # rhof_1LUT.ApplyPreset('Linear Green (Gr4L)', True)


    # # get opacity transfer function/opacity map for 'rhof_1'
    # rhof_1PWF = GetOpacityTransferFunction('rhof_1')

    # # get 2D transfer function for 'rhof_1'
    # rhof_1TF2D = GetTransferFunction2D('rhof_1')
    # rhof_1TF2D.RescaleTransferFunction(-0.236462214961648, 0.6000000238418579, -0.236462214961648, 0.6000000238418579)

    # get color transfer function/color map for 'rhof_1'
    rhof_1LUT = GetColorTransferFunction('rhof_1')

    # Rescale transfer function
    rhof_1LUT.RescaleTransferFunction(-0.20031742751598358, 0.6000000238418579)

    # get opacity transfer function/opacity map for 'rhof_1'
    rhof_1PWF = GetOpacityTransferFunction('rhof_1')

    # Rescale transfer function
    rhof_1PWF.RescaleTransferFunction(-0.20031742751598358, 0.6000000238418579)

    # get 2D transfer function for 'rhof_1'
    rhof_1TF2D = GetTransferFunction2D('rhof_1')

    # Rescale 2D transfer function
    rhof_1TF2D.RescaleTransferFunction(-0.20031742751598358, 0.6000000238418579, -0.20031742751598358, 0.6000000238418579)

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    rhof_1LUT.ApplyPreset('Linear Green (Gr4L)', True)



    # rename source object
    RenameSource('surface', contour1_2)

    # set active source
    SetActiveSource(output60000vts)

    # create a new 'Calculator'
    calculator1 = Calculator(registrationName='Calculator1', Input=output60000vts)

    # Properties modified on calculator1
    calculator1.ResultArrayName = 'Wind'
    calculator1.Function = 'iHat*u+jHat*v+kHat*w'

    # show data in view
    calculator1Display = Show(calculator1, renderView1, 'StructuredGridRepresentation')

    # trace defaults for the display properties.
    calculator1Display.Representation = 'Outline'

    # hide data in view
    Hide(output60000vts, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Stream Tracer'
    streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=calculator1,
        SeedType='Line')

    # set active source
    SetActiveSource(streamTracer1)

    # show data in view
    streamTracer1Display = Show(streamTracer1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    streamTracer1Display.Representation = 'Surface'

    # show color bar/color legend
    streamTracer1Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'u'
    uLUT = GetColorTransferFunction('u')

    # get opacity transfer function/opacity map for 'u'
    uPWF = GetOpacityTransferFunction('u')

    # get 2D transfer function for 'u'
    uTF2D = GetTransferFunction2D('u')

    # toggle interactive widget visibility (only when running from the GUI)
    ShowInteractiveWidgets(proxy=streamTracer1.SeedType)

    # Properties modified on streamTracer1
    streamTracer1.SeedType = 'Point Cloud'

    # show data in view
    streamTracer1Display = Show(streamTracer1, renderView1, 'GeometryRepresentation')

    # show color bar/color legend
    streamTracer1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # update the view to ensure updated data information
    renderView1.Update()

    # Rescale transfer function
    uLUT.RescaleTransferFunction(-7.26479959487915, 24.676965713500977)

    # Rescale transfer function
    uPWF.RescaleTransferFunction(-7.26479959487915, 24.676965713500977)

    # set scalar coloring
    ColorBy(streamTracer1Display, ('POINTS', 'Wind', 'Magnitude'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(uLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    streamTracer1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    streamTracer1Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'Wind'
    windLUT = GetColorTransferFunction('Wind')

    # get opacity transfer function/opacity map for 'Wind'
    windPWF = GetOpacityTransferFunction('Wind')

    # get 2D transfer function for 'Wind'
    windTF2D = GetTransferFunction2D('Wind')

    # set active source
    SetActiveSource(contour1_2)

    # toggle interactive widget visibility (only when running from the GUI)
    HideInteractiveWidgets(proxy=streamTracer1.SeedType)

    #================================================================
    # addendum: following script captures some of the application
    # state to faithfully reproduce the visualization during playback
    #================================================================

    # get layout
    layout1 = GetLayout()

    #--------------------------------
    # saving layout sizes for layouts

    # layout/tab size in pixels
    layout1.SetSize(773, 739)

    #-----------------------------------
    # saving camera placements for views
    renderView1.CameraPosition = [1620.2599173277679, 2875.71028142868, 1677.3782503162731]
    renderView1.CameraFocalPoint = [18.313435762431503, 33.49998570198864, 478.3742527245868]
    renderView1.CameraViewUp = [-0.2169492255886175, -0.27308791755751294, 0.9372064995509796]
    renderView1.CameraViewAngle = 32.29589535408209
    renderView1.CameraParallelScale = 899.6336487402332

    ##--------------------------------------------
    ## You may need to add some code at the end of this python script depending on your usage, eg:
    #
    ## Render all views to see them appears
    # RenderAllViews()
    #
    ## Interact with the view, usefull when running from pvpython
    # Interact()
    #
    ## Save a screenshot of the active view
    # SaveScreenshot("path/to/screenshot.png")
    #
    ## Save a screenshot of a layout (multiple splitted view)
    SaveScreenshot(output_file, GetLayout())
    #
    ## Save all "Extractors" from the pipeline browser
    # SaveExtracts()
    #
    ## Save a animation of the current active view
    # SaveAnimation()
    #
    ## Please refer to the documentation of paraview.simple
    ## https://www.paraview.org/paraview-docs/latest/python/paraview.simple.html
    ##--------------------------------------------


if __name__ == '__main__':
    render()