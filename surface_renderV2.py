import vtk
import numpy as np

def create_surface_actor():
    # Step 1: Read the .vts file (structured grid)
    reader = vtk.vtkXMLStructuredGridReader()
    reader.SetFileName("C:\\Users\\Gebruiker\\Desktop\\Visualization\\wildfire_svvr\\data\\output.1000.vts")
    reader.Update()

    # Step 2: Extract the surface of the structured grid
    extractSurface = vtk.vtkDataSetSurfaceFilter()
    extractSurface.SetInputConnection(reader.GetOutputPort())
    extractSurface.Update()

    # Step 3: Crop the side facing the camera (along the Z-axis)
    # bounds = extractSurface.GetOutput().GetBounds()
    # cropPlane = vtk.vtkPlane()
    # cropPlane.SetOrigin(bounds[0], bounds[2], bounds[5] - (bounds[5] - bounds[4]) * 0.8)  # Position crop origin near the front (camera-facing side)
    # cropPlane.SetNormal(0, 0, -1)  # Crop in the negative Z direction

    # No cropping applied
    cropPlane = vtk.vtkPlane()  # Create a plane but do not use it for cropping

    # Apply the cropping using vtkClipPolyData
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(extractSurface.GetOutputPort())
    clipper.SetClipFunction(cropPlane)
    clipper.Update()

    # Step 4: Adjust the scalar range to avoid issues with logarithmic scaling
    data = clipper.GetOutput()
    scalars = data.GetPointData().GetScalars()
    scalar_range = scalars.GetRange()

    # Step 5: Set up color mapping
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clipper.GetOutputPort())
    mapper.SetScalarRange(scalar_range)

    # Create color map with green for high values and brown for low values
    lookup_table = vtk.vtkLookupTable()
    lookup_table.SetNumberOfTableValues(256)
    lookup_table.SetRange(scalar_range)  # Use the updated range

    # Linear interpolation
    r_values = np.linspace(0, 0.65, 256)  # Interpolate between green (0.0, 1.0, 0.0) and brown (0.65, 0.33, 0.0)
    g_values = np.linspace(1, 0.33, 256)
    b_values = np.linspace(0, 0, 256)

    # Make give more contrast to high values
    first_segment_length = 200
    total_length = 256
    remaining_length = total_length - first_segment_length

    # Define small step size for the first segment
    r_values_first = np.linspace(0.65, 0.4, first_segment_length) 
    g_values_first = np.linspace(0.3, 5, first_segment_length)

    # Define larger step size for the second segment
    r_values_second = np.linspace(0.4, 0.0, remaining_length)
    g_values_second = np.linspace(0.5, 1, remaining_length)

    # Combine the two segments
    r_values = np.concatenate([r_values_first, r_values_second])
    g_values = np.concatenate([g_values_first, g_values_second])

    b_values = np.zeros(total_length)

    for i, rgb in enumerate(zip(r_values, g_values, b_values)):
        r, g, b = rgb
        lookup_table.SetTableValue(i, r, g, b, 1.0)
    lookup_table.Build()

    # Set the color map to the mapper
    mapper.SetLookupTable(lookup_table)
    mapper.SetColorModeToMapScalars()

    # Step 6: Create the actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

if __name__ == "__main__":
    actor = create_surface_actor()

    # Step 7: Set up rendering
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the renderer
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)  # Set background color

    # Adjust the camera to fit the data
    renderer.ResetCamera()

    # Step 8: Render and start interaction
    renderWindow.Render()
    renderWindowInteractor.Start()
