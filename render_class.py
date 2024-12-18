from paraview.simple import *


class renderer:
    def __init__(self):
        self.setup_window()

    def setup_window(self):
        paraview.simple._DisableFirstRenderCameraReset()

        # load state
        LoadState("data\\states\\double_wind_clean.pvsm")

        # find view
        self.renderView1 = FindViewOrCreate("RenderView1", viewtype="RenderView")

        # set active view
        SetActiveView(self.renderView1)

        # find source NOTE: has to be same as used in the state for some reason.
        self.output60000vts = FindSource("output.40000.vts")

        # set active source
        SetActiveSource(self.output60000vts)

        # get display properties
        output60000vtsDisplay = GetDisplayProperties(
            self.output60000vts, view=self.renderView1
        )

    def plot(
        self,
        path_to_file,
        side_output_file,
        topdown_output_file,
        wind_origins_p1_start,
        wind_origins_p1_end,
        wind_origins_p2_start,
        wind_origins_p2_end,
    ):
        print("Rendering:", path_to_file)

        output_vts = GetActiveSource()

        ReplaceReaderFileName(
            output_vts,
            [path_to_file],
            "FileName",
        )

        streamTracer1 = FindSource("StreamTracer1")
        streamTracer1.SeedType.Point1 = wind_origins_p1_start
        streamTracer1.SeedType.Point2 = wind_origins_p1_end

        streamTracer2 = FindSource("StreamTracer2")
        streamTracer2.SeedType.Point1 = wind_origins_p2_start
        streamTracer2.SeedType.Point2 = wind_origins_p2_end

        # get layout
        layout1 = GetLayout()

        # layout/tab size in pixels
        layout1.SetSize(972, 719)

        # Sideways angle camera placement
        self.renderView1.CameraPosition = [1230.4102702553741, 3195.8994642793778, 1215.362951668812]
        self.renderView1.CameraFocalPoint = [100.99999999999999, -0.9999999999999812, 449.68107392152956]
        self.renderView1.CameraViewUp = [-0.07399763649576889, -0.20748228371695188, 0.9754360315964541]
        self.renderView1.CameraParallelScale = 899.6336487402332

        # SaveScreenshot(side_output_file)

        # Top-down view
        self.renderView1.CameraPosition = [78.53204961242727, 29.374903765884817, 3925.393236573283]
        self.renderView1.CameraFocalPoint = [101.0, -0.9999999999999997, 449.6810739215296]
        self.renderView1.CameraViewUp = [-5.648797798927756e-05, -0.9999618170748182, 0.008738489659899696]
        self.renderView1.CameraParallelScale = 899.6336487402332

        SaveScreenshot(topdown_output_file)


# if __name__ == '__main__':
#     render()
