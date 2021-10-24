from manimlib import *
from scipy import signal as sig


class TimeDependentComplexPlane(ComplexPlane):
    CONFIG = {
        "dimension": 3,
        "t_range": np.array([0., 5., 1.]),
        "t_axis_config": {
            "include_ticks": True,
        },
        "background_line_style": {
            "stroke_color": GREY_D,
        },
        "depth": 8,
    }

    def __init__(self, **kwargs):
        ComplexPlane.__init__(self, **kwargs)

        t_axis = self.create_axis(self.t_range, self.t_axis_config, self.depth)
        t_axis.rotate(-PI / 2, UP, about_point=ORIGIN)
        t_axis.shift(self.n2p(0))

        self.t_axis = t_axis
        self.add(t_axis)
        self.axes.add(t_axis)

    def number_to_point(self, number, time=0):
        return self.coords_to_point(number.real, number.imag, time)

    def n2p(self, number, time=0):
        return self.number_to_point(number, time)

    def get_t_axis(self):
        return self.axes[2]

    def get_graph(self, function, axis, t_range=None, **kwargs):
        # sample range
        s_range = np.array(self.t_range, dtype=float)

        if t_range is not None:
            s_range[:len(t_range)] = t_range

        if t_range is None or len(t_range) < 3:
            s_range[2] /= self.num_sampled_graph_points_per_tick

        graph = ParametricCurve(
            lambda t: self.t_axis.number_to_point(t) + axis.number_to_point(function(t)),
            t_range=s_range,
            **kwargs
        )
        graph.underlying_function = function
        graph.t_range = t_range
        return graph

    def get_inphase_graph(self, function, **kwargs):
        return self.get_graph(function, self.get_x_axis(), **kwargs)

    def get_quadrature_graph(self, function, **kwargs):
        return self.get_graph(function, self.get_y_axis(), **kwargs)


class QamModulation(Scene):
    CONFIG = {}

    def construct(self):
        cplane = TimeDependentComplexPlane()

        self.play(ShowCreation(cplane))
        self.play(self.camera.frame.animate.move_to(2 * OUT))

        graph_y = cplane.get_inphase_graph(lambda t: 2 * np.cos(2 * t), color=RED)
        graph_x = cplane.get_quadrature_graph(lambda t: 1 * sig.square(4 * t), color=BLUE)

        self.play(self.camera.frame.animate.reorient(90, 90, 90))
        self.play(ShowCreation(graph_x))

        self.play(self.camera.frame.animate.reorient(0, 90, 90))
        self.play(ShowCreation(graph_y))

        self.play(self.camera.frame.animate.reorient(80, 90, 90))

        # arrow = Arrow(

        # open an interactive IPython shell here
        self.embed()
