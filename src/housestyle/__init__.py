"""housestyle: paper figures in the mshipping MATLAB house style, drawn with matplotlib.

    import housestyle as hs
    fig, axes = hs.figure(2, 4)
    for k, ax in enumerate(axes.flat):
        hs.irf(ax, h, med[:, k], lo[:, k], hi[:, k], names[k], 'Std', 'Months')
    hs.export(fig, 'irf_baseline')
"""
from ._style import (BAND, DATA, FOURTH, GREY, INK, LATEX_SCALE, MAIN, RC, SECOND, STACK,
                     THIRD, YELLOW, use)
from .core import (band, bars, colorbar, event, export, figure, finish, fit, hline, irf, legend,
                   line, note, outdir, shade, tex, tickaligned, vline, years, yyaxis, zero)

__version__ = "1.1.0"

__all__ = [
    "figure", "fit", "finish", "legend", "years", "tex", "yyaxis", "colorbar", "tickaligned",
    "irf", "line", "band", "zero", "shade", "event", "bars", "note", "hline", "vline",
    "outdir", "export", "use", "RC", "LATEX_SCALE",
    "MAIN", "BAND", "DATA", "SECOND", "THIRD", "FOURTH", "GREY", "YELLOW", "STACK", "INK",
]
