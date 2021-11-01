import sys, os
import numpy as np

nsamples = 300

np.seterr(over='raise')

def tap(c, tau, f):
    return np.exp(2j * np.pi * f * tau)


# attenuations for frequency plot
f_whole = np.logspace(5, 9, num=nsamples)
linear_whole = 1 / f_whole
multipath_whole = tap(c=.8, tau=500e-9, f=f_whole) + tap(c=.4, tau=300e-9, f=f_whole)
channel_whole = linear_whole * multipath_whole

# coordinates for complex diagram
f_tap = np.linspace(2e6, 2.5e6, num=nsamples)
linear_tap = 1 / f_tap

multipath_tap_1 = tap(c=.8, tau=500e-9, f=f_tap)
multipath_tap_2 = tap(c=.4, tau=300e-9, f=f_tap)
multipath_taps = multipath_tap_1 + multipath_tap_2

data = np.array(list(zip(f_whole, linear_whole, np.abs(channel_whole),
        np.real(multipath_tap_1), np.imag(multipath_tap_1),
        np.real(multipath_tap_2), np.imag(multipath_tap_2),
        np.real(multipath_taps), np.imag(multipath_taps))))

# save to file
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
name, _ = os.path.splitext(os.path.basename(__file__))
filename = os.path.join(location, name + ".dat")
np.savetxt(filename, data, fmt='%.6e')
