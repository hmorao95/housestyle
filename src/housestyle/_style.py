"""Colors, sizes and matplotlib settings that reproduce the MATLAB house style.

Font sizes are calibrated against MATLAB R2026a export_fig output of the same figures
(matlab/images): with tick labels at 10 pt the two match to the pixel, titles measure
13.2 pt, and LaTeX labels and legends measure 10.25 and 10 pt in matplotlib's
Computer Modern. Line widths are in points in both. Dash patterns scale with line
width, as measured: dashes 4 widths on and 4 off, dash-dot 4-1-2-1.
"""
from __future__ import annotations

import matplotlib as mpl
from cycler import cycler

RGB = tuple[float, float, float]

# palette (mshipping regen_fig_confound.m and the acid-shock paper figures)
MAIN: RGB = (0.0, 0.0, 0.0)          # point estimate, baseline, model: solid, 2 pt
BAND: RGB = (0.0, 0.5, 1.0)          # credible band, alpha 0.5
DATA: RGB = (0.0, 0.4470, 0.7410)    # one observed series: solid, 1.5 pt
SECOND: RGB = (0.85, 0.33, 0.10)     # orange, dashed, 1.8 pt
THIRD: RGB = (0.10, 0.60, 0.10)      # green, dash-dot, 1.8 pt
FOURTH: RGB = (0.49, 0.18, 0.56)     # purple, solid with dots, 1.2 pt
GREY: RGB = (0.5, 0.5, 0.5)          # reference lines, shaded episodes
YELLOW: RGB = (0.93, 0.69, 0.13)
STACK: tuple[RGB, ...] = (BAND, SECOND, YELLOW, GREY, THIRD)   # stacked bars
INK: RGB = (0.1294, 0.1294, 0.1294)  # MATLAB R2026a text and axes color, #212121

# MATLAB geometry: figure pixels are screen pixels at 96 per inch
PX_PER_INCH = 96.0
WIDTH_PX = 1180
ROW_PX = 285
DPI = 300

# font sizes in points, measured from the MATLAB output
AXES_PT = 12.0
TITLE_PT = 13.2      # bold Arial
LABEL_PT = 10.25     # LaTeX-interpreted axis labels
TICK_PT = 10.0
LEGEND_PT = 10.9     # LaTeX-interpreted legend text
EVENT_PT = 8.0

SANS = ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]

RC: dict[str, object] = {
    "figure.facecolor": "white",
    "figure.dpi": PX_PER_INCH,
    "savefig.facecolor": "white",
    "savefig.dpi": DPI,
    "font.family": "sans-serif",
    "font.sans-serif": SANS,
    "font.size": AXES_PT,
    "mathtext.fontset": "cm",
    "axes.facecolor": "white",
    "axes.edgecolor": INK,
    "axes.linewidth": 0.5,
    "axes.labelcolor": INK,
    "axes.labelsize": LABEL_PT,
    "axes.labelpad": 4.0,
    "axes.titlesize": TITLE_PT,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "text.color": INK,
    "legend.labelcolor": INK,
    "axes.titlepad": 2.0,
    "axes.grid": True,
    "axes.axisbelow": True,
    "axes.unicode_minus": False,
    "axes.autolimit_mode": "round_numbers",
    "axes.xmargin": 0.0,
    "axes.ymargin": 0.0,
    "axes.prop_cycle": cycler(color=[DATA, SECOND, YELLOW, FOURTH, THIRD]),
    "grid.color": INK,
    "grid.alpha": 0.15,
    "grid.linewidth": 0.5,
    "grid.linestyle": "-",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.labelsize": TICK_PT,
    "ytick.labelsize": TICK_PT,
    "xtick.color": INK,
    "ytick.color": INK,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.pad": 4.0,
    "ytick.major.pad": 3.0,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    "lines.linewidth": 0.5,
    "lines.scale_dashes": True,
    "lines.dashed_pattern": (4.0, 4.0),
    "lines.dashdot_pattern": (4.0, 1.0, 2.0, 1.0),
    "lines.solid_joinstyle": "round",
    "lines.solid_capstyle": "butt",
    "lines.dash_capstyle": "butt",
    "patch.linewidth": 0.5,
    "legend.fontsize": LEGEND_PT,
    "legend.fancybox": False,
    "legend.framealpha": 1.0,
    "legend.edgecolor": INK,
    "legend.handlelength": 2.75,     # 30 pt line sample, MATLAB ItemTokenSize
    "legend.handleheight": 0.85,
    "legend.handletextpad": 0.37,
    "legend.borderpad": 0.28,
    "legend.labelspacing": 0.25,
    "legend.columnspacing": 0.8,
}


def use() -> None:
    """Apply the house style to matplotlib globally. figure() calls it for you."""
    mpl.rcParams.update(RC)
