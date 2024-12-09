import vtk
import numpy as np
import plotly.graph_objects as go
from tqdm import tqdm  # Import tqdm for the loading bar

def create_o2_actor(subsample_fraction=0.001):
    # Load the dataset
    reader = vtk.vtkXMLStructuredGridReader()
    reader.SetFileName("data/output.1000.vts")
    reader.Update()
    data = reader.GetOutput()
    point_data = data.GetPointData()

    # Extract the O2 data array
    o2_array = point_data.GetArray("O2")

    # Get the points from the dataset
    points = data.GetPoints()

    # Add progress bars for point extraction
    total_points = points.GetNumberOfPoints()
    coords = np.array([points.GetPoint(i) for i in tqdm(range(total_points), desc="Extracting coordinates")])

    # Add progress bar for O2 value extraction
    o2_values = np.array([o2_array.GetValue(i) for i in tqdm(range(o2_array.GetNumberOfTuples()), desc="Extracting O2 values")])

    # Show the total number of points
    print(f"Total number of points: {total_points}")

    # Subsample the points (e.g., 10% of the total points)
    num_subsample = int(total_points * subsample_fraction)
    indices = np.random.choice(total_points, num_subsample, replace=False)  # Randomly select indices

    subsampled_coords = coords[indices]
    subsampled_o2_values = o2_values[indices]

    # Create a VTK points object and add the subsampled coordinates
    vtk_points = vtk.vtkPoints()
    for coord in subsampled_coords:
        vtk_points.InsertNextPoint(coord)

    # Create a VTK polydata object and set the points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(vtk_points)

    # Create a VTK array for the O2 values and add the subsampled O2 values
    vtk_o2_values = vtk.vtkFloatArray()
    vtk_o2_values.SetName("O2")
    for value in subsampled_o2_values:
        vtk_o2_values.InsertNextValue(value)

    # Add the O2 values array to the polydata
    polydata.GetPointData().AddArray(vtk_o2_values)
    polydata.GetPointData().SetActiveScalars("O2")

    # Create a VTK vertex glyph filter to visualize the points
    glyph_filter = vtk.vtkVertexGlyphFilter()
    glyph_filter.SetInputData(polydata)
    glyph_filter.Update()

    # Create a mapper and actor for the points
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph_filter.GetOutputPort())
    mapper.SetScalarRange(subsampled_o2_values.min(), subsampled_o2_values.max())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

