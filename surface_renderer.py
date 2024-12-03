from utils import *
import numpy as np
import os
import vtk
from vtk.util.numpy_support import numpy_to_vtk


def renderSurface(renderer, rawDataset, dataset, name):
    vtkArray = numpy_to_vtk(dataset[name])
    grid = vtk.vtkStructuredGrid()
    grid.CopyStructure(rawDataset)
    grid.GetPointData().SetScalars(vtkArray)
    
    surfaceMapper = vtk.vtkDataSetMapper()
    surfaceMapper.SetInputData(grid)
    # surfaceMapper.SetLookupTable(colormap.properties[name])
    surfaceMapper.Update()

    actor = vtk.vtkActor()
    actor.SetMapper(surfaceMapper)
    actor.GetProperty().SetRepresentationToSurface()

    renderer.AddActor(actor)

    return grid

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
    render_handler.update_renderer(renderer)
    render_handler.show()


if __name__ == "__main__":
    main()