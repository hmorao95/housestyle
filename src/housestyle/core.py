"""Drawing helpers: figure, panels, marks, labels and export in the house style."""
from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PolyCollection
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from matplotlib.text import Annotation
from matplotlib.ticker import FixedFormatter, FixedLocator, FuncFormatter, ScalarFormatter

from . import _style as S
from ._style import use

# MATLAB subplot geometry (subplot.m): DefaultAxesPosition and the cell insets
_DEFAULT_POS = (0.13, 0.11, 0.775, 0.815)
_INSET = (0.2, 0.18, 0.04, 0.1)          # left, bottom, right, top, as cell fractions

_SERIES: dict[Any, dict[str, Any]] = {
    1: dict(color=S.MAIN, linewidth=2.0, linestyle="-"),
    2: dict(color=S.SECOND, linewidth=1.8, linestyle="--"),
    3: dict(color=S.THIRD, linewidth=1.8, linestyle="-."),
    4: dict(color=S.FOURTH, linewidth=1.2, linestyle="-", marker="o", markersize=3.5,
            markerfacecolor=S.FOURTH, markeredgecolor=S.FOURTH),
    "data": dict(color=S.DATA, linewidth=1.5, linestyle="-"),
}
_SERIES_NAMES = {"main": 1, "second": 2, "third": 3, "fourth": 4, "data": "data"}

_outdir: Path | None = None


# ---- figure and panels ---------------------------------------------------------

def figure(rows: int = 1, cols: int = 4, height: float | None = None,
           width: float = S.WIDTH_PX) -> tuple[Figure, Any]:
    """New figure with a rows x cols grid of panels, placed as MATLAB's subplot places them.

    Sizes are MATLAB figure pixels (96 per inch): 1180 px wide and 30 + 285*rows px
    tall by default, so fonts keep the same size relative to the panels. Returns
    (fig, axes): one Axes for a 1 x 1 grid, a 1-D array for one row or column, else a
    2-D array indexed [row, col]. Loop with ``for ax in axes.flat``.

    Typical grids: figure(1, 4), figure(2, 4), and figure(1, 1, 460) for one wide panel.
    """
    use()
    if height is None:
        height = 30 + S.ROW_PX * rows
    fig = plt.figure(figsize=(width / S.PX_PER_INCH, height / S.PX_PER_INCH),
                     dpi=S.PX_PER_INCH)
    grid = np.empty((rows, cols), dtype=object)
    for r in range(rows):
        for c in range(cols):
            inner, cell = _subplot_boxes(rows, cols, r, c)
            ax = fig.add_axes(inner)
            ax._housestyle_cell = cell        # read by fit()
            ax._housestyle_inner = inner
            ax.grid(True)
            ax.set_axisbelow(True)
            ax.tick_params(which="both", direction="in", top=True, right=True)
            grid[r, c] = ax
    if rows * cols == 1:
        return fig, grid[0, 0]
    if rows == 1 or cols == 1:
        return fig, grid.ravel()
    return fig, grid


def _subplot_boxes(nrows: int, ncols: int, r: int, c: int
                   ) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    """Inner axes box (x, y, w, h) and its cell (x0, y0, x1, y1), MATLAB subplot.m rules."""
    left, bottom, width, height = _DEFAULT_POS
    w = width / (ncols - _INSET[0] - _INSET[2])
    h = height / (nrows - _INSET[1] - _INSET[3])
    rb = nrows - 1 - r                       # MATLAB counts rows from the top
    x0, y0 = left + c * w, bottom + rb * h
    iw, ih = w * (1 - _INSET[0] - _INSET[2]), h * (1 - _INSET[1] - _INSET[3])
    cx0 = 0.0 if c == 0 else x0 - _INSET[0] * w
    cy0 = 0.0 if rb == 0 else y0 - _INSET[1] * h
    cx1 = 1.0 if c == ncols - 1 else x0 + iw + _INSET[2] * w
    cy1 = 1.0 if rb == nrows - 1 else y0 + ih + _INSET[3] * h
    return (x0, y0, iw, ih), (cx0, cy0, cx1, cy1)


def fit(fig: Figure) -> None:
    """Shrink panels whose labels, title or legend overflow their subplot cell.

    MATLAB keeps each panel's decorations inside its cell and shrinks the plot box when
    they do not fit. export() calls this; call it yourself before plt.show() or a
    direct savefig.
    """
    axs = [ax for ax in fig.axes if hasattr(ax, "_housestyle_cell")]
    if not axs:
        return
    for _ in range(2):
        fig.draw_without_rendering()
        renderer = fig.canvas.get_renderer()
        to_fig = fig.transFigure.inverted()
        for ax in axs:
            cx0, cy0, cx1, cy1 = ax._housestyle_cell
            x, y, w, h = ax._housestyle_inner
            pos = ax.get_position()
            default = (x - cx0, y - cy0, cx1 - (x + w), cy1 - (y + h))
            extra = ax.get_default_bbox_extra_artists()
            south = getattr(ax, "_housestyle_south_legend", None)
            if south is not None and south in extra:
                # MATLAB reserves the legend's height below the cell's usual margin
                leg = south.get_window_extent(renderer).transformed(to_fig)
                cy0 += leg.height + 6 / 72 * fig.dpi / fig.bbox.height
                extra = [a for a in extra if a is not south]
            tb = ax.get_tightbbox(renderer, bbox_extra_artists=extra).transformed(to_fig)
            need = (pos.x0 - tb.x0, pos.y0 - tb.y0, tb.x1 - pos.x1, tb.y1 - pos.y1)
            m = [max(d, n) for d, n in zip(default, need)]
            ax.set_position([cx0 + m[0], cy0 + m[1],
                             max(cx1 - m[2] - cx0 - m[0], 0.05 * w),
                             max(cy1 - m[3] - cy0 - m[1], 0.05 * h)])


# ---- labels --------------------------------------------------------------------

_MATLAB_ESCAPES = {r"\%": "%", r"\$": "$", r"\&": "&", r"\#": "#", r"\_": "_"}
# characters that cannot sit inside \text{} in mathtext; & ^ ~ can
_MATH_ESCAPES = {"#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "\\": r"\backslash"}


def tex(s: str) -> str:
    """A label as MATLAB's LaTeX interpreter draws it: Computer Modern roman text.

    Text between a pair of $ signs stays math, e.g. '$100\\times\\log$'. A lone $ is a
    dollar sign. MATLAB escapes such as '\\%' and '\\$' are accepted, so labels port
    unchanged from MATLAB scripts.
    """
    if s is None or s == "":
        return s
    dollars = [m.start() for m in re.finditer(r"(?<!\\)\$", s)]
    if dollars and len(dollars) % 2 == 0:
        chunks, last = [], 0
        for a, b in zip(dollars[::2], dollars[1::2]):
            chunks += [(False, s[last:a]), (True, s[a + 1:b])]
            last = b + 1
        chunks.append((False, s[last:]))
    else:
        chunks = [(False, s)]
    out = []
    for is_math, chunk in chunks:
        if is_math:
            out.append(chunk)
            continue
        for k, v in _MATLAB_ESCAPES.items():
            chunk = chunk.replace(k, v)
        run = ""
        for ch in chunk:
            if ch in _MATH_ESCAPES:
                if run:
                    out.append(_text_run(run))
                    run = ""
                out.append(_MATH_ESCAPES[ch])
            else:
                run += ch
        if run:
            out.append(_text_run(run))
    return "$" + "".join(out) + "$"


def _text_run(run: str) -> str:
    return r"\text{" + run.replace("%", r"\%").replace("$", r"\$") + "}"


def _matlab_number(v: float, pos: int | None = None) -> str:
    """Tick label as MATLAB writes it: 0, 0.5, -0.4, 1000 (no trailing zeros)."""
    if abs(v) < 1e-12:
        return "0"
    s = f"{v:.6g}"
    if "e" in s:
        s = f"{v:.10f}".rstrip("0").rstrip(".") if abs(v) < 1 else f"{v:.0f}"
    return s


def finish(ax: Axes, title: str | None = None, ylabel: str | None = None,
           xlabel: str | None = None, zero: bool = True) -> None:
    """Title, labels, ticks and zero line for a finished panel.

    title   plain bold title, sentence case, no units
    ylabel  y label with units ('Std', '%', 'USD/t, 2016 $'), drawn as LaTeX text
    xlabel  x label, e.g. 'Months'
    zero    draw the dashed zero line when 0 lies inside the y-limits

    Tick labels become MATLAB numbers; a date x axis gets year ticks; more than five
    y ticks are thinned to every other one, keeping 0. finish() fixes the y-limits, so
    draw everything first.
    """
    if title:
        ax.set_title(title, fontsize=S.TITLE_PT, fontweight="bold", color=S.INK)
    if ylabel:
        ax.set_ylabel(tex(ylabel), fontsize=S.LABEL_PT, color=S.INK)
    if xlabel:
        ax.set_xlabel(tex(xlabel), fontsize=S.LABEL_PT, color=S.INK)
    for axis in (ax.xaxis, ax.yaxis):
        if isinstance(axis.get_major_formatter(), ScalarFormatter):
            axis.set_major_formatter(FuncFormatter(_matlab_number))
    if isinstance(ax.xaxis.get_major_locator(), mdates.AutoDateLocator):
        years(ax)
    if zero:
        _draw_zero(ax)
    _thin_yticks(ax)
    bb = ax.get_window_extent()
    length = 0.01 * max(bb.width, bb.height) * 72 / ax.figure.dpi   # MATLAB TickLength
    ax.tick_params(which="major", length=length, labelsize=S.TICK_PT)


def _thin_yticks(ax: Axes) -> None:
    lo, hi = ax.get_ylim()
    eps = 1e-9 * max(1.0, abs(hi - lo))
    loc, fmt = ax.yaxis.get_major_locator(), ax.yaxis.get_major_formatter()
    ticks = np.asarray(ax.get_yticks(), dtype=float)
    labels = None
    if isinstance(loc, FixedLocator) and isinstance(fmt, FixedFormatter) \
            and len(fmt.seq) == len(loc.locs):
        labels = list(fmt.seq)
    keep_in = (ticks >= lo - eps) & (ticks <= hi + eps)
    t = ticks[keep_in]
    if t.size <= 5:
        return
    z = np.flatnonzero(np.abs(t) < 1e-12 * max(1.0, np.abs(t).max()))
    start = int(z[0] % 2) if z.size else 0
    kept = t[start::2]
    if labels is not None:
        lab = [s for s, k in zip(labels, keep_in) if k][start::2]
        ax.set_yticks(kept, labels=lab)
    else:
        ax.set_yticks(kept)
    ax.set_ylim(lo, hi)


def years(ax: Axes, base: int | None = None, fmt: str = "%Y") -> None:
    """Year ticks on a date x axis, every `base` years (default: about one per 0.6 inch)."""
    if base is None:
        lo, hi = ax.get_xlim()
        span = (hi - lo) / 365.25
        width_in = ax.get_position().width * ax.figure.get_figwidth()
        max_ticks = max(2, int(width_in / 0.6))
        base = next((b for b in (1, 2, 5, 10, 20, 25, 50, 100) if span / b <= max_ticks), 100)
    ax.xaxis.set_major_locator(mdates.YearLocator(base))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))


def legend(ax: Axes, handles: Sequence[Any] | None = None, labels: Sequence[str] | None = None,
           loc: str = "best", outside: str | None = None, ncols: int | None = None,
           **kwargs: Any) -> Legend:
    """Legend in the house style: LaTeX text, square box, white fill. One panel only.

    outside='south' puts it below the axes in one row, under the tick labels, as
    MATLAB's 'southoutside' does (for stacked bars). Call it after finish().
    """
    if handles is None:
        handles, auto = ax.get_legend_handles_labels()
        labels = auto if labels is None else labels
    elif labels is None:
        labels = [h.get_label() for h in handles]
    labels = [tex(lab) for lab in labels]
    opts: dict[str, Any] = dict(loc=loc, prop={"size": S.LEGEND_PT}, fancybox=False,
                                framealpha=1.0, edgecolor=S.INK)
    if outside == "south":
        ax.figure.draw_without_rendering()
        r = ax.figure.canvas.get_renderer()
        below_px = ax.bbox.y0 - ax.xaxis.get_tightbbox(r).y0
        below_pt = max(below_px, 0) * 72 / ax.figure.dpi + 6
        opts.update(loc="upper center", bbox_to_anchor=(0.5, 0), bbox_transform=ax.transAxes,
                    borderaxespad=below_pt / S.LEGEND_PT, ncols=ncols or len(labels))
    elif outside is not None:
        raise ValueError("outside must be None or 'south'")
    elif ncols:
        opts["ncols"] = ncols
    opts.update(kwargs)
    leg = ax.legend(handles, labels, **opts)
    leg.get_frame().set_linewidth(0.5)
    ax._housestyle_south_legend = leg if outside == "south" else None
    return leg


# ---- marks ---------------------------------------------------------------------

def line(ax: Axes, x: Any, y: Any, k: int | str = 1, **kwargs: Any) -> Line2D:
    """Series k in the house order, so line style and color both identify it.

    1 or 'main'     black solid, 2 pt          baseline, point estimate, model
    2 or 'second'   orange dashed, 1.8 pt
    3 or 'third'    green dash-dot, 1.8 pt
    4 or 'fourth'   purple solid with dots, 1.2 pt
    'data'          MATLAB blue solid, 1.5 pt  one observed series on its own

    No fifth style and no dotted style (dots vanish in print): use small multiples.
    Extra keywords go to ax.plot, e.g. label='Baseline'.
    """
    key = _SERIES_NAMES.get(k.lower(), None) if isinstance(k, str) else k
    if key not in _SERIES:
        if isinstance(k, int) and k > 4:
            raise ValueError("The house style has four line series. Use small multiples.")
        raise ValueError(f"Unknown series {k!r}. Use 1 to 4, or 'data'.")
    style = {**_SERIES[key], "zorder": 2, **kwargs}
    (h,) = ax.plot(x, y, **style)
    return h


def band(ax: Axes, x: Any, lo: Any, hi: Any, color: Any = S.BAND,
         alpha: float = 0.5) -> PolyCollection:
    """Credible or confidence band, blue at alpha 0.5, kept out of the legend.

    Draw the point estimate first: the band lies over it, so the black line reads navy.
    """
    return ax.fill_between(x, lo, hi, facecolor=color, alpha=alpha, edgecolor="none",
                           linewidth=0, zorder=2, label="_nolegend_")


def zero(ax: Axes) -> Line2D | None:
    """Dashed zero line under the data, only when 0 lies strictly inside the y-limits."""
    if getattr(ax, "_housestyle_zero", None) is not None:
        return ax._housestyle_zero
    lo, hi = ax.get_ylim()
    if not lo < 0 < hi:
        return None
    ln = ax.axhline(0, color="k", linewidth=0.5, linestyle="--", zorder=1.5,
                    label="_nolegend_")
    ax.set_ylim(lo, hi)
    ax._housestyle_zero = ln
    return ln


_draw_zero = zero        # finish() has a flag named zero


def irf(ax: Axes, h: Any, med: Any, lo: Any = None, hi: Any = None, title: str | None = None,
        ylabel: str | None = None, xlabel: str | None = None, *,
        finish_panel: bool = True) -> tuple[Line2D, PolyCollection | None]:
    """One impulse-response panel: black median, blue band over it, zero line, labels.

    h = 0 is impact, so text that quotes h = 0, 6, 12 matches the axis. Pass lo and hi
    as None for no band. With finish_panel=False, draw more series and call finish().
    Returns the line and band handles.
    """
    h = np.asarray(h)
    hl = line(ax, h, med, 1)
    hb = band(ax, h, lo, hi) if lo is not None and hi is not None else None
    ax.set_xlim(h.min(), h.max())
    if finish_panel:
        finish(ax, title, ylabel, xlabel)
    return hl, hb


def shade(ax: Axes, x0: Any, x1: Any, label: str | None = None, color: Any = S.GREY,
          alpha: float = 0.15) -> Polygon:
    """Grey shaded episode (a war, a recession) over the full height, behind the data.

    x0 and x1 may be dates. Give a label to list it in the legend.
    """
    return ax.axvspan(x0, x1, facecolor=color, alpha=alpha, edgecolor="none", linewidth=0,
                      zorder=1, label=label if label else "_nolegend_")


def event(ax: Axes, x: Any, y: float, label: str | Sequence[str] | None = None,
          ha: str = "center") -> tuple[Line2D, Annotation | None]:
    """Black dot at (x, y) with a short 8 pt label, above the dot when y >= 0.

    label may be a list of lines. ha sets the alignment: 'center', 'left' or 'right'.
    Leave headroom above a peak, or the label runs into the title.
    """
    (dot,) = ax.plot([x], [y], "o", color="k", markerfacecolor="k", markersize=4,
                     zorder=3, label="_nolegend_")
    if not label:
        return dot, None
    if not isinstance(label, str):
        label = "\n".join(label)
    dy = 0.03 * ax.bbox.height * 72 / ax.figure.dpi
    up = y >= 0
    txt = ax.annotate(label, (x, y), xytext=(0, dy if up else -dy), textcoords="offset points",
                      ha=ha, va="bottom" if up else "top", multialignment=ha,
                      fontsize=S.EVENT_PT, color=S.INK, zorder=3)
    return dot, txt


def bars(ax: Axes, x: Any, Y: Any, labels: Sequence[str] | None = None,
         colors: Sequence[Any] = S.STACK, width: float | None = None) -> list[BarContainer]:
    """Stacked bars, one column of Y per component (historical decompositions).

    Positive parts stack up from zero and negative parts stack down, as MATLAB does.
    Bars touch (width = the smallest spacing of x) and have no edges. x may be dates.
    """
    Y = np.asarray(Y, dtype=float)
    if Y.ndim == 1:
        Y = Y[:, None]
    xs = np.asarray(x)
    xn = mdates.date2num(xs) if np.issubdtype(xs.dtype, np.datetime64) or \
        (xs.dtype == object and hasattr(xs.flat[0], "year")) else xs.astype(float)
    if width is None:
        width = float(np.min(np.diff(np.sort(xn)))) if len(xn) > 1 else 0.8
    pos, neg = np.zeros(len(xn)), np.zeros(len(xn))
    out = []
    for j in range(Y.shape[1]):
        y = Y[:, j]
        base = np.where(y >= 0, pos, neg)
        cont = ax.bar(x, y, width=width, bottom=base, color=colors[j % len(colors)],
                      edgecolor="none", linewidth=0, zorder=2,
                      label=labels[j] if labels else "_nolegend_")
        out.append(cont)
        pos = pos + np.where(y >= 0, y, 0)
        neg = neg + np.where(y < 0, y, 0)
    return out


# ---- output --------------------------------------------------------------------

def outdir(path: str | Path | None = None) -> Path:
    """Get or set the folder export() writes bare names to (default: the current folder).

    outdir('figures') sets it and creates it; outdir('') resets it.
    """
    global _outdir
    if path is None:
        return _outdir if _outdir is not None else Path.cwd()
    if str(path) == "":
        _outdir = None
        return Path.cwd()
    p = Path(path).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    _outdir = p
    return p


def export(fig: Figure, name: str | Path, *, dpi: int = S.DPI, fit_panels: bool = True,
           close: bool = False, **kwargs: Any) -> Path:
    """Save at 300 dpi on white, cropped to the content as export_fig does.

    export(fig, 'fig1') writes fig1.png to outdir(). A name with a folder or a suffix
    ('figs/fig1.pdf') is used as given. Extra keywords go to fig.savefig.
    Returns the path written.
    """
    p = Path(name)
    if p.suffix == "":
        p = p.with_suffix(".png")
    if not p.is_absolute() and p.parent == Path("."):
        p = outdir() / p
    p.parent.mkdir(parents=True, exist_ok=True)
    if fit_panels:
        fit(fig)
    opts: dict[str, Any] = dict(dpi=dpi, bbox_inches="tight", pad_inches=0.01,
                                facecolor="white")
    opts.update(kwargs)
    fig.savefig(p, **opts)
    if close:
        plt.close(fig)
    return p
