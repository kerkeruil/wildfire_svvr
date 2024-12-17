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

    def plot(self, filename, output_file):
        ReplaceReaderFileName(
            self.output60000vts,
            [
                f"C:\\Users\\Gebruiker\\Desktop\\Visualization\\wildfire_svvr\\data\\raw\\{filename}"
            ],
            "FileName",
        )

        # get layout
        layout1 = GetLayout()

        # layout/tab size in pixels
        layout1.SetSize(1156, 739)

        # current camera placement for renderView1
        self.renderView1.CameraPosition = [
            1644.8866840337323,
            1790.212856596348,
            2090.833388367462,
        ]
        self.renderView1.CameraFocalPoint = [
            181.2758156667214,
            79.14277344119773,
            306.9464359719487,
        ]
        self.renderView1.CameraViewUp = [
            -0.25623357300275595,
            -0.5839189046402611,
            0.7703136172170132,
        ]
        self.renderView1.CameraViewAngle = 25.398878827080637
        self.renderView1.CameraParallelScale = 899.6336487402332

        SaveScreenshot(output_file, GetLayout())


# if __name__ == '__main__':
#     render()
