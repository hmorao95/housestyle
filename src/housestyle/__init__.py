"""housestyle: paper figures in the mshipping MATLAB house style, drawn with matplotlib.

    import housestyle as hs
    fig, axes = hs.figure(2, 4)
    for k, ax in enumerate(axes.flat):
        hs.irf(ax, h, med[:, k], lo[:, k], hi[:, k], names[k], 'Std', 'Months')
    hs.export(fig, 'irf_baseline')
"""
from ._style import (BAND, DATA, FOURTH, GREY, INK, MAIN, RC, SECOND, STACK, THIRD, YELLOW,
                     use)
from .core import (band, bars, event, export, figure, finish, fit, irf, legend, line, outdir,
                   shade, tex, years, zero)

__version__ = "1.0.0"

__all__ = [
    "figure", "fit", "finish", "legend", "years", "tex",
    "irf", "line", "band", "zero", "shade", "event", "bars",
    "outdir", "export", "use", "RC",
    "MAIN", "BAND", "DATA", "SECOND", "THIRD", "FOURTH", "GREY", "YELLOW", "STACK", "INK",
]
