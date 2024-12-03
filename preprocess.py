from utils import *
import numpy as np
import os
from pathlib import Path

# With help from https://github.com/stuartheeb/wildfire-visualization/blob/master/preprocess.py
# TODO: change variablenames 


def preprocess(filename="data/output.1000.vts"):
    print("Preprocessing data...")
    raw_data = readin_vts(filename)

    # General variables TODO: check how it works
    bounds = np.array(raw_data.GetBounds()) 
    extent = np.array(raw_data.GetExtent())
    resampledOrigin = bounds[::2]
    resampledPointsDims = np.array([300, 250, 150], dtype=int)
    resampledCellsDims = resampledPointsDims - 1
    resampledCellSpacing = (bounds[1::2] - bounds[:-1:2]) / resampledCellsDims

    # Grass data TODO: check how it works
    extractorGrass = vtk.vtkExtractGrid()
    extractorGrass.SetInputData(raw_data)
    extractorGrass.SetVOI(extent[0], extent[1], extent[2], extent[3], 0, 10)
    extractorGrass.Update()
    datasetGrass = extractorGrass.GetOutput()    
    grassBounds = np.array(datasetGrass.GetBounds())
    grassPointsDims = np.array([300, 250, 200], dtype=int)
    grassCellsDims = grassPointsDims - 1
    grassCellSpacing = (grassBounds[1::2] - grassBounds[:-1:2]) / grassCellsDims
    resamplerGrass = vtk.vtkResampleToImage()
    resamplerGrass.AddInputDataObject(datasetGrass)
    resamplerGrass.SetSamplingDimensions(grassPointsDims)  ### set for #points
    resamplerGrass.SetSamplingBounds(bounds)
    resamplerGrass.Update()
    grassVtkArray = resamplerGrass.GetOutput().GetPointData().GetArray('rhof_1')

    # Soil data TODO: check how it works
    empty_soil_grid = vtk.vtkExtractGrid()
    empty_soil_grid.SetInputData(raw_data)
    empty_soil_grid.SetVOI(extent[0], extent[1], extent[2], extent[3], 0, 5)
    empty_soil_grid.Update()
    soil_grid = vtk.vtkStructuredGrid()
    soil_grid.CopyStructure(empty_soil_grid.GetOutput())
    soilVtkArray = empty_soil_grid.GetOutput().GetPointData().GetArray('rhof_1')
    soil_grid.GetPointData().SetScalars(soilVtkArray)

    processed_data = {
        'bounds': bounds,
        'extent': extent,
        'resampledOrigin': resampledOrigin,
        'resampledPointsDims': resampledPointsDims,
        'resampledCellSpacing': resampledCellSpacing,
        'grassPointsDims': grassPointsDims,
        'grassCellSpacing': grassCellSpacing,
        'soil': soil_grid
    }

    ret = {}
    ret['extent'] = extent
    ret['resampledOrigin'] = resampledOrigin
    ret['resampledPointsDims'] = resampledPointsDims
    ret['resampledCellSpacing'] = resampledCellSpacing
    ret['grassPointsDims'] = grassPointsDims
    ret['grassCellSpacing'] = grassCellSpacing
    ret['soil'] = soilVtkArray
    ret['grass'] = grassVtkArray
    # ret['theta'] = thetaVtkArray
    # ret['vapor'] = vaporVtkArray
    # ret['windVelocityMag'] = windVelMagVtkArray
    # ret['windVelocity'] = windVelocityVtkArray
    # ret['vorticity'] = vortVtkArray

    return ret

if __name__ == "__main__":
    data_folder = "data"
    filename = "output.1000.vts"
    processed_data = preprocess()

    os.makedirs(Path(data_folder, "preprocessed"), exist_ok=True)
    np.savez(Path(data_folder, "preprocessed", f"{filename[:-4]}.npz"), **processed_data)
