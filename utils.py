import vtk
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera


def readin_vts(filename):
    data = vtk.vtkXMLStructuredGridReader()
    data.SetFileName(filename)
    data.Update()
    return data.GetOutput()

class VTK_Renderer():
    def __init__(self):
        self.renderWindow = vtk.vtkRenderWindow()
        self.renderWindow.SetSize(800, 600)

         # Set interaction methods
        self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)

        renderer = vtk.vtkRenderer()
        renderer.SetViewport(0, 0, 0.0, 0.0)
        renderer.SetBackground(0.0, 0.0, 0.0)

        self.update_renderer(renderer)

    def get_renderer(self):
        return vtk.vtkRenderer()

    def update_renderer(self, renderer):
        self.renderWindow.AddRenderer(renderer)

    def show(self):
        self.renderWindow.Render()
        self.renderWindowInteractor.Start()

       