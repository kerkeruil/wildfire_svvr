from paraview.simple import *


class renderer:
    def __init__(self, state_file="data\\states\\ideal_state.pvsm"):
        self.state_file = state_file
        self.setup_window()

    def setup_window(self):
        paraview.simple._DisableFirstRenderCameraReset()

        # load state
        LoadState("data\\states\\ideal_state.pvsm")

        # find view
        self.renderView1 = FindViewOrCreate("RenderView1", viewtype="RenderView")

        # set active view
        SetActiveView(self.renderView1)

        # find source
        self.output60000vts = FindSource("output.60000.vts")

        # set active source
        SetActiveSource(self.output60000vts)

        # get display properties
        output60000vtsDisplay = GetDisplayProperties(
            self.output60000vts, view=self.renderView1
        )

    def plot(self, path_to_file, side_output_file, topdown_output_file, wind_origin=[246, -10, 191]):
        print("Rendering:", path_to_file)

        
        output_vts = GetActiveSource()
        
        ReplaceReaderFileName(
            output_vts,
            [
                path_to_file
            ],
            "FileName",
        )

        streamTracer1 = FindSource('StreamTracer2')
        print(wind_origin)
        streamTracer1.SeedType.Center = wind_origin


        # get layout
        layout1 = GetLayout()

        # layout/tab size in pixels
        layout1.SetSize(1156, 739)

        # Sideways angle camera placement 
        self.renderView1.CameraPosition = [1230.4102702553741, 3195.8994642793778, 1215.362951668812]
        self.renderView1.CameraFocalPoint = [100.99999999999999, -0.9999999999999812, 449.68107392152956]
        self.renderView1.CameraViewUp = [-0.07399763649576889, -0.20748228371695188, 0.9754360315964541]
        self.renderView1.CameraParallelScale = 899.6336487402332

        SaveScreenshot(side_output_file)

        # Top-down view
        self.renderView1.CameraPosition = [123.437929897274, -0.9961992340726892, 3925.5261539655476]
        self.renderView1.CameraFocalPoint = [101.0, -0.999999999999997, 449.6810739215296]
        self.renderView1.CameraViewUp = [-0.0003387769050458798, 0.9999999426145049, 1.0934568858827726e-06]
        self.renderView1.CameraParallelScale = 899.6336487402332

        SaveScreenshot(topdown_output_file)



# if __name__ == '__main__':
#     render()
