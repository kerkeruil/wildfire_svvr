from utils import *
import numpy as np
import os
import vtk
from vtk.util.numpy_support import numpy_to_vtk



def renderSurface(renderer, rawDataset, dataset, name):
    # Convert NumPy array to VTK format
    vtkArray = numpy_to_vtk(dataset[name])
    
    # Create the structured grid and assign scalars
    grid = vtk.vtkStructuredGrid()
    grid.CopyStructure(rawDataset)
    grid.GetPointData().SetScalars(vtkArray)
    
    # Create a lookup table for scalar-to-color mapping
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(256)  # Number of colors in the table
    lut.SetRange(dataset[name].min(), dataset[name].max())  # Scalar range
    lut.Build()
    
    # Optionally customize the colors (e.g., gradient from blue to red)
    for i in range(256):
        lut.SetTableValue(i, i / 255.0, 1.0 - i / 255.0, 0.5, 1.0)  # RGBA
    
    # Create the mapper and assign the grid and lookup table
    surfaceMapper = vtk.vtkDataSetMapper()
    surfaceMapper.SetInputData(grid)
    surfaceMapper.SetLookupTable(lut)
    surfaceMapper.SetScalarRange(dataset[name].min(), dataset[name].max())  # Match the scalar range
    
    # Create the actor and set its properties
    actor = vtk.vtkActor()
    actor.SetMapper(surfaceMapper)
    actor.GetProperty().SetRepresentationToSurface()
    
    # Add the actor to the renderer
    renderer.AddActor(actor)
    
    return grid


def renderVolume(renderer, dataset, name, origin, dimensions, spacing):
    vtkArray = numpy_to_vtk(dataset[name])
    image = vtk.vtkImageData()
    image.SetOrigin(origin)
    image.SetDimensions(dimensions)
    image.SetSpacing(spacing)
    image.GetPointData().SetScalars(vtkArray)

    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetInputData(image)
    volumeMapper.Update()

    actor = vtk.vtkVolume()
    actor.SetMapper(volumeMapper)
    # actor.SetProperty(colormap.properties[name])
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(0.5, 0.0, 1.0, 0.0)
    colorTransferFunction.AddRGBPoint(1.0, 0.0, 0.5, 0.0)

    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0.0, 0.0)
    opacityTransferFunction.AddPoint(0.5, 0.5)
    opacityTransferFunction.AddPoint(1.0, 1.0)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    actor.SetProperty(volumeProperty)

    renderer.AddActor(actor)

    return image, actor

def main():
    render_handler = VTK_Renderer()

    dataset = np.load(os.path.join("data", 'preprocessed/output.1000.npz'))
    extent = dataset["extent"]

    raw_data = vtk.vtkXMLStructuredGridReader()
    raw_data.SetFileName(os.path.join("data/", 'output.1000.vts'))
    raw_data.Update()

    extractor = vtk.vtkExtractGrid()
    extractor.SetInputConnection(raw_data.GetOutputPort())
    extractor.SetVOI(extent[0], extent[1], extent[2], extent[3], 0, 5)
    extractor.Update()

    renderer = render_handler.get_renderer()

    soilSurface = renderSurface(renderer, extractor.GetOutput(), dataset, 'soil')
    # grassImage, _ = renderVolume(renderer, dataset, 'grass', dataset["resampledOrigin"], dataset["grassPointsDims"], dataset["grassCellSpacing"])
    
    render_handler.update_renderer(renderer)
    render_handler.show()


if __name__ == "__main__":
    main()