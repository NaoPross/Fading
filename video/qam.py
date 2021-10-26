from manimlib import *
from scipy import signal as sig

def square(t, slew_rate=.1):
    t = t % 1

    if t < .1:
        return t * 1 / slew_rate
    elif t < .5 - slew_rate / 2:
        return 1
    elif t < .5 + slew_rate / 2:
        return 1 - (t - (.5 - slew_rate / 2)) * 1 / slew_rate
    else:
        return 0


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

    def point_to_number(self, point, time=0):
        return point[0] + 1j * point[1]

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
        self.camera.frame.reorient(0, 0, 0)

        # create a complex plane
        cplane = TimeDependentComplexPlane()
        self.play(ShowCreation(cplane))

        # a complex number
        dot = Dot(cplane.n2p(1 + 2j), color=GREEN)

        number = DecimalNumber()

        number.add_updater(lambda m: m.next_to(dot, RIGHT))

        def update_nums(m):
            x, y, z = dot.get_center()
            num = cplane.p2n((x,y))
            m.set_value(num)

        number.add_updater(update_nums)

        # create and move complex number around
        self.play(ShowCreation(dot), ShowCreation(number))
        self.play(dot.animate.move_to(cplane.n2p(-5+3j)), run_time=2)
        self.play(dot.animate.move_to(cplane.n2p(-4-3j)), run_time=2)

        # move the number according to a time dependend complex function
        def signal_func(t):
            real = -2 * np.cos(2 * t)
            imag = 3 * (square(t / 2) - .5)

            return real + 1j * imag

        signal_func_at_zero = signal_func(0)

        self.play(dot.animate.move_to(cplane.n2p(signal_func_at_zero)), run_time=2)

        def dot_update_func(m, dt):
            m.move_to(cplane.n2p(signal_func(m.time)))
            m.time = m.time + dt / 2

        dot.time = 0
        dot.add_updater(dot_update_func)
        self.wait(5)

        # get out and show time dependence
        self.play(self.camera.frame.animate.shift(2 * OUT))

        # show functions
        graph_y = cplane.get_inphase_graph(lambda t: signal_func(t).real, color=RED)
        graph_x = cplane.get_quadrature_graph(lambda t: signal_func(t).imag, color=BLUE)

        self.play(self.camera.frame.animate.reorient(-90, 90, 90))
        self.play(ShowCreation(graph_x))

        self.play(self.camera.frame.animate.reorient(0, 90, 90))
        self.play(ShowCreation(graph_y))

        self.play(self.camera.frame.animate.reorient(-100, 90, 90))
        self.play(self.camera.frame.animate.rotate(40 * DEGREES, axis = UP))

        # create arrow for complex value
        dot.remove_updater(dot_update_func)
        self.play(dot.animate.move_to(cplane.n2p(signal_func_at_zero)), run_time=2)

        arr = Arrow(cplane.n2p(0), cplane.n2p(signal_func_at_zero))
        self.play(ShowCreation(arr))

        def arr_update_func(m, dt):
            m.set_points_by_ends(
                cplane.n2p(0, time=m.time),
                cplane.n2p(signal_func(m.time), time=m.time)
            )
            m.time = m.time + dt / 2

        dot.time = 0
        arr.time = 0

        dot.add_updater(dot_update_func)
        arr.add_updater(arr_update_func)
        self.wait(10)

        self.play(*map(FadeOut, (arr, graph_x, graph_y)))
        self.play(
            self.camera.frame.animate.rotate(50 * DEGREES, axis = UP),
            dot.animate.move_to(cplane.n2p(1+1j))
        )
        self.play(self.camera.frame.animate.shift(-2 * OUT))

        dot.remove_updater(dot_update_func)
        arr.remove_updater(arr_update_func)

        # open an interactive IPython shell here
        # self.embed()
