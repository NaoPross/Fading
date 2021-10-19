from manimlib import *

class QamModulation(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        circle = Circle()
        self.play(FadeIn(circle))
        self.wait(3)

        # open an interactive IPython shell here
        self.embed()
