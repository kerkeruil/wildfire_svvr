import vtk
import numpy as np

def create_wind_actor(filename='data/output.1000.vts', glyph_size=15.0, clip_perc=0.9):    
    # Read the dataset
    datasetReader = vtk.vtkXMLStructuredGridReader()
    datasetReader.SetFileName(filename)
    datasetReader.Update()
    dataset = datasetReader.GetOutput()

    # ----------- Global Variables ------------
    bounds = np.array(dataset.GetBounds()) 
    extent = np.array(dataset.GetExtent())
    resampledOrigin = bounds[::2]
    
    # Reduce resolution (if needed)
    resampledPointsDims = np.array([100, 100, 100], dtype=int)  # Reduce resolution
    resampledCellsDims = resampledPointsDims - 1
    resampledCellSpacing = (bounds[1::2] - bounds[:-1:2]) / resampledCellsDims
    resampler = vtk.vtkResampleToImage()
    resampler.AddInputDataObject(dataset)
    resampler.SetSamplingDimensions(resampledPointsDims)
    resampler.SetSamplingBounds(bounds)
    resampler.Update()
    ImageData = resampler.GetOutput()

    # ------------------ velocity magnitude -----------------------
    calcMag = vtk.vtkArrayCalculator()
    calcMag.SetInputData(ImageData)
    calcMag.AddScalarVariable('u_var', 'u', 0)
    calcMag.AddScalarVariable('v_var', 'v', 0)
    calcMag.AddScalarVariable('w_var', 'w', 0)
    calcMag.SetResultArrayName('wind_velocity_mag')
    calcMag.SetFunction('sqrt(u_var^2+v_var^2+w_var^2)')
    calcMag.SetAttributeTypeToPointData()
    calcMag.Update()
    windVelMagVtkArray = calcMag.GetOutput().GetPointData().GetArray('wind_velocity_mag')

    # ------------------ velocity vector --------------------------
    calcCompose = vtk.vtkArrayCalculator()
    calcCompose.SetInputConnection(calcMag.GetOutputPort())
    calcCompose.AddScalarVariable('u_var', 'u', 0)
    calcCompose.AddScalarVariable('v_var', 'v', 0)
    calcCompose.AddScalarVariable('w_var', 'w', 0)
    calcCompose.SetResultArrayName('wind_velocity')
    calcCompose.SetFunction('u_var*iHat+v_var*jHat+w_var*kHat')
    calcCompose.SetAttributeTypeToPointData()
    calcCompose.Update()
    windVelocityVtkArray = calcCompose.GetOutput().GetPointData().GetArray('wind_velocity')

    # ------------------ Create Arrow Glyphs ----------------
    # Create an arrow source for the glyphs
    arrowSource = vtk.vtkArrowSource()
    
    # Create a Glyph3D filter
    glyph3D = vtk.vtkGlyph3D()
    glyph3D.SetInputData(ImageData)
    glyph3D.SetSourceConnection(arrowSource.GetOutputPort())
    glyph3D.SetVectorModeToUseVector()
    glyph3D.SetScaleModeToDataScalingOff()  # Scale based on the magnitude of the vector field
    
    # Set the scale factor to make the glyphs larger
    glyph3D.SetScaleFactor(glyph_size)  # Adjust this value to make glyphs bigger or smaller
    
    # Optional: Set color mode to color by vector (if you want color representation of direction)
    glyph3D.SetColorModeToColorByVector()
    
    # ------------------ Clipping Plane ---------------------
   # Define a plane to clip 90% from the top of the dataset
    clippingPlane = vtk.vtkPlane()
    clippingPlane.SetOrigin(bounds[0], bounds[2], bounds[5])  # Origin at the top of the dataset
    clippingPlane.SetNormal(0, 0, -1)  # Clip along the Z axis (vertical direction), with a negative normal
    
    # Move the clipping plane 90% downwards along the Z-axis
    clipDistance = clip_perc * (bounds[5] - bounds[4])  # 60% of the height of the dataset
    clippingPlane.SetOrigin(bounds[0], bounds[2], bounds[5] - clipDistance)  # Update origin

    # Create a clipper to apply the plane
    clipper = vtk.vtkClipPolyData()
    clipper.SetClipFunction(clippingPlane)
    clipper.SetInputConnection(glyph3D.GetOutputPort())
    clipper.Update()

    # ------------------ Mapper and Actor ----------------
    # Mapper for the clipped glyphs
    glyphMapper = vtk.vtkPolyDataMapper()
    glyphMapper.SetInputConnection(clipper.GetOutputPort())
    
    # Actor for the glyphs
    glyphActor = vtk.vtkActor()
    glyphActor.SetMapper(glyphMapper)

    return glyphActor

if __name__ == '__main__':
    actor = create_wind_actor('data/output.1000.vts')

    # ------------------ Rendering ------------------------
    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the glyph actor to the renderer
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)  # Dark background for better contrast


    # Start the rendering process
    renderWindow.Render()
    renderWindowInteractor.Start()

    # Call the wind_renderer function to render the wind glyphs
