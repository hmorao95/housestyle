"""Unit tests for housestyle. Run from the package root: py -m pytest"""
from __future__ import annotations

import datetime as dt

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402
from PIL import Image  # noqa: E402

import housestyle as hs  # noqa: E402


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")
    hs.outdir("")


# ---- figure and panels -------------------------------------------------------

def test_figure_size_matches_matlab_pixels():
    fig, axes = hs.figure(2, 4)
    w, h = fig.get_size_inches() * 96
    assert (round(w), round(h)) == (1180, 600)
    assert axes.shape == (2, 4)


def test_subplot_geometry_matches_matlab():
    # MATLAB subplot(2,4,1) Position: [0.1300 0.5838 0.1566 0.3412]
    fig, axes = hs.figure(2, 4)
    x, y, w, h = axes[0, 0].get_position().bounds
    assert (x, y, w, h) == pytest.approx((0.13, 0.5838, 0.1566, 0.3412), abs=2e-4)


def test_figure_squeezes_like_subplots():
    _, ax = hs.figure(1, 1, 460)
    assert isinstance(ax, matplotlib.axes.Axes)
    _, row = hs.figure(1, 4)
    assert row.shape == (4,)


def test_axes_settings():
    _, ax = hs.figure(1, 1)
    assert ax.xaxis._major_tick_kw.get("gridOn", True)
    assert ax.get_axisbelow() is True
    assert matplotlib.rcParams["xtick.direction"] == "in"
    assert matplotlib.rcParams["ytick.right"] is True


# ---- labels and ticks ----------------------------------------------------------

@pytest.mark.parametrize("label, expected", [
    ("Std", r"$\text{Std}$"),
    (r"\%", r"$\text{\%}$"),
    ("%", r"$\text{\%}$"),
    ("USD/t, 2016 $", r"$\text{USD/t, 2016 \$}$"),
    (r"USD/t, 2016 \$", r"$\text{USD/t, 2016 \$}$"),
    (r"$100\times\log$", r"$100\times\log$"),
    ("a & b_1", r"$\text{a & b}\_\text{1}$"),
    ("{x} #2", r"$\{\text{x}\}\text{ }\#\text{2}$"),
])
def test_tex(label, expected):
    assert hs.tex(label) == expected


def test_tex_labels_render():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [0, 1])
    hs.finish(ax, "Title", "USD/t, 2016 $", r"$100\times\log$ & more_x {y} ~ ^")
    ax.figure.canvas.draw()


def test_finish_labels_and_fonts():
    _, ax = hs.figure(1, 1)
    ax.plot([1, 2, 3])
    hs.finish(ax, "Oil", "%", "Months")
    assert ax.get_title() == "Oil"
    assert ax.title.get_fontweight() == "bold"
    assert ax.title.get_fontsize() == pytest.approx(13.2)        # measured from MATLAB
    assert ax.yaxis.label.get_fontsize() == pytest.approx(10.25)
    assert ax.xaxis.get_ticklabels()[0].get_fontsize() == pytest.approx(10)


def test_tick_labels_are_matlab_numbers():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [-0.5, 1.0])
    hs.finish(ax)
    ax.figure.canvas.draw()
    text = [t.get_text() for t in ax.get_yticklabels()]
    assert "0" in text
    assert not any(s.endswith(".0") or "−" in s for s in text)   # no 0.0, hyphen minus
    assert any(s.startswith("-") for s in text)


def test_thinning_keeps_zero_and_limits():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [-3, 3])
    ax.set_ylim(-3, 3)
    ax.set_yticks(np.arange(-3, 4))
    hs.finish(ax)
    assert list(ax.get_yticks()) == [-2, 0, 2]
    assert ax.get_ylim() == (-3, 3)


def test_thinning_manual_labels():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [1, 7])
    ax.set_ylim(1, 7)
    ax.set_yticks(range(1, 8), labels=list("abcdefg"))
    hs.finish(ax, zero=False)
    assert [t.get_text() for t in ax.get_yticklabels()] == list("aceg")


def test_years_auto_base():
    _, axes = hs.figure(1, 2, 380)
    t = mdates.date2num([dt.date(2015, 1, 1), dt.date(2026, 6, 1)])
    axes[0].plot(mdates.num2date(t), [1, 2])
    axes[0].set_xlim(t)
    hs.finish(axes[0])
    loc = axes[0].xaxis.get_major_locator()
    assert isinstance(loc, mdates.YearLocator)
    assert loc.base.step == 2


# ---- marks ---------------------------------------------------------------------

def test_irf_panel():
    _, ax = hs.figure(1, 1)
    h = np.arange(13)
    m = np.exp(-h / 4)
    hl, hb = hs.irf(ax, h, m, m - 0.3, m + 0.3, "Oil", "Std", "Months")
    assert ax.get_xlim() == (0, 12)
    assert hl.get_color() == (0, 0, 0) or hl.get_color() == hs.MAIN
    assert hl.get_linewidth() == 2
    assert tuple(hb.get_facecolor()[0]) == pytest.approx((0, 0.5, 1, 0.5))
    assert hb.zorder == hl.zorder
    kids = ax.get_children()
    assert kids.index(hb) > kids.index(hl)              # band over the line: navy
    assert ax._housestyle_zero is not None
    assert ax._housestyle_zero.zorder < hl.zorder        # zero line under the data


def test_irf_without_band():
    _, ax = hs.figure(1, 1)
    _, hb = hs.irf(ax, range(7), np.ones(7) + 1)
    assert hb is None


def test_zero_line_only_inside_limits():
    _, ax = hs.figure(1, 1)
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.set_ylim(1, 3)
    assert hs.zero(ax) is None
    _, ax = hs.figure(1, 1)
    ax.plot([1, 2, 3], [-1, 0.5, 1])
    ln = hs.zero(ax)
    assert ln.get_linestyle() == "--" and ln.get_linewidth() == 0.5


def test_line_styles():
    _, ax = hs.figure(1, 1)
    x = [1, 2, 3]
    h1, h2, h3 = hs.line(ax, x, x, 1), hs.line(ax, x, x, "second"), hs.line(ax, x, x, 3)
    h4, hd = hs.line(ax, x, x, 4), hs.line(ax, x, x, "data", label="Observed")
    assert (h1.get_linestyle(), h1.get_linewidth()) == ("-", 2)
    assert (h2.get_linestyle(), h2.get_color()) == ("--", hs.SECOND)
    assert (h3.get_linestyle(), h3.get_color()) == ("-.", hs.THIRD)
    assert h4.get_marker() == "o"
    assert hd.get_color() == hs.DATA and hd.get_label() == "Observed"
    assert ":" not in {h.get_linestyle() for h in (h1, h2, h3, h4, hd)}


def test_dash_patterns_scale_with_width_like_matlab():
    assert matplotlib.rcParams["lines.dashed_pattern"] == [4.0, 4.0]
    assert matplotlib.rcParams["lines.dashdot_pattern"] == [4.0, 1.0, 2.0, 1.0]
    assert matplotlib.rcParams["lines.scale_dashes"] is True


def test_line_errors():
    _, ax = hs.figure(1, 1)
    with pytest.raises(ValueError, match="four line series"):
        hs.line(ax, [1], [1], 5)
    with pytest.raises(ValueError, match="Unknown series"):
        hs.line(ax, [1], [1], "fifth")


def test_shade_and_event_with_dates():
    _, ax = hs.figure(1, 1)
    x = [dt.date(2020, 1, 1) + dt.timedelta(days=30 * i) for i in range(24)]
    y = np.sin(np.arange(24))
    ax.plot(x, y)
    p = hs.shade(ax, dt.date(2021, 1, 1), dt.date(2021, 6, 1), label="War")
    assert p.get_alpha() == pytest.approx(0.15) and p.zorder < 2
    dot, txt = hs.event(ax, x[4], 0.5, ["Two", "lines"])
    assert dot.get_marker() == "o" and txt.get_fontsize() == 8
    assert txt.get_text() == "Two\nlines" and txt.get_va() == "bottom"
    _, txt = hs.event(ax, x[5], -0.5, "Below")
    assert txt.get_va() == "top"


def test_bars_stack_positive_up_negative_down():
    _, ax = hs.figure(1, 1)
    x = np.arange(3)
    Y = np.array([[1.0, -1.0], [2.0, 3.0], [-2.0, -1.0]])
    c1, c2 = hs.bars(ax, x, Y, labels=["a", "b"])
    r = c2.patches
    assert (r[0].get_y(), r[0].get_height()) == (0, -1)      # first negative: from 0
    assert (r[1].get_y(), r[1].get_height()) == (2, 3)       # on top of 2
    assert (r[2].get_y(), r[2].get_height()) == (-2, -1)     # below -2
    assert c1.patches[0].get_width() == pytest.approx(1.0)
    assert tuple(c1.patches[0].get_facecolor()[:3]) == pytest.approx(hs.STACK[0])


def test_bars_with_dates():
    _, ax = hs.figure(1, 1)
    x = np.array(["2020-01-01", "2020-02-01", "2020-03-01"], dtype="datetime64[D]")
    (c,) = hs.bars(ax, x, [1.0, -1.0, 2.0])
    assert c.patches[0].get_width() == pytest.approx(29)        # shortest month gap


# ---- legend and layout ---------------------------------------------------------

def test_legend_style():
    _, ax = hs.figure(1, 1)
    a = hs.line(ax, [0, 1], [0, 1], 1)
    b = hs.line(ax, [0, 1], [1, 0], 2)
    leg = hs.legend(ax, [a, b], ["Baseline", "More lags"])
    assert leg.get_frame().get_linewidth() == 0.5
    assert leg.get_texts()[0].get_text() == r"$\text{Baseline}$"


def test_legend_outside_south_sits_below_tick_labels():
    fig, ax = hs.figure(1, 1, 460)
    x = np.arange(10)
    cs = hs.bars(ax, x, np.random.default_rng(0).normal(size=(10, 3)), labels=list("abc"))
    hs.finish(ax, "T", "Std")
    leg = hs.legend(ax, [c for c in cs], list("abc"), outside="south")
    h0 = ax.get_position().height
    hs.fit(fig)
    fig.draw_without_rendering()
    r = fig.canvas.get_renderer()
    assert leg.get_window_extent(r).y1 <= ax.xaxis.get_tightbbox(r).y0 + 1
    assert leg._ncols == 3
    # the plot box gives up at least the legend's height, as MATLAB's does
    leg_h = leg.get_window_extent(r).height / fig.bbox.height
    assert ax.get_position().height <= h0 - leg_h


def test_fit_keeps_labels_inside_cell():
    fig, axes = hs.figure(1, 4)
    for ax in axes:
        ax.plot([0, 24], [-1, 1])
        hs.finish(ax, "A long enough title", "Std", "Months")
    hs.fit(fig)
    r = fig.canvas.get_renderer()
    to_fig = fig.transFigure.inverted()
    for ax in axes:
        tb = ax.get_tightbbox(r).transformed(to_fig)
        assert tb.y0 >= -1e-3 and tb.y1 <= 1 + 1e-3


# ---- output --------------------------------------------------------------------

def test_outdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    d = hs.outdir("sub")
    assert d == tmp_path / "sub" and d.is_dir()
    monkeypatch.chdir(tmp_path / "sub")
    assert hs.outdir() == d                       # a later chdir does not move it
    assert hs.outdir("") == tmp_path / "sub"


def test_export_png_at_300_dpi(tmp_path):
    hs.outdir(tmp_path)
    fig, ax = hs.figure(1, 1)
    hs.irf(ax, range(13), np.linspace(1, -1, 13), "Oil", "Std", "Months")
    out = hs.export(fig, "t1")
    assert out == tmp_path / "t1.png" and out.is_file()
    with Image.open(out) as im:
        assert im.width > 2500                        # 1180 px at 300 dpi, cropped
        assert round(im.info["dpi"][0]) == 300
        assert im.getpixel((2, 2))[:3] == (255, 255, 255)


def test_export_respects_folder_and_suffix(tmp_path):
    fig, ax = hs.figure(1, 1)
    ax.plot([0, 1])
    out = hs.export(fig, tmp_path / "figs" / "f.pdf", close=True)
    assert out.suffix == ".pdf" and out.is_file()
    assert not plt.fignum_exists(fig.number)


# ---- 1.1: MATLAB behaviours the paper figures needed ----------------------------

def test_tickaligned_stops_at_data_when_padding_is_large():
    # data -0.003 .. 0.104, MATLAB step 0.05: -0.05 would pad 44 percent of the range,
    # 0.15 would pad 43 percent, so both limits stop at the data
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [-0.003, 0.104])
    hs.tickaligned(ax, 0.05)
    assert ax.get_ylim() == pytest.approx((-0.003, 0.104))
    assert list(ax.get_yticks()) == pytest.approx([0, 0.05, 0.1])


def test_tickaligned_rounds_out_when_padding_is_small():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [-0.48, 1.04])
    hs.tickaligned(ax, 0.5)
    assert ax.get_ylim() == pytest.approx((-0.5, 1.04))     # 0.02 kept, 0.46 too much
    hs.finish(ax, zero=False)                                # finish keeps the limits
    assert ax.get_ylim() == pytest.approx((-0.5, 1.04))


def test_tickaligned_default_step_is_current_spacing():
    _, ax = hs.figure(1, 1)
    ax.plot([0, 1], [0.0, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    hs.tickaligned(ax)
    assert list(ax.get_yticks()) == pytest.approx([0, 0.25, 0.5, 0.75, 1.0])


def test_hline_vline_match_matlab_constant_lines():
    _, ax = hs.figure(1, 1)
    hs.line(ax, [0, 1], [0, 1], 1)
    top = hs.hline(ax, 0.5)
    under = hs.vline(ax, 0.5, color="k", linestyle="--", layer="bottom")
    assert top.get_alpha() == pytest.approx(0.7) and top.get_linewidth() == 0.5
    assert top.zorder > 2 > under.zorder
    assert under.get_linestyle() == "--"
    assert top.get_label() == "_nolegend_"


def test_note_is_latex_at_matlab_size():
    _, ax = hs.figure(1, 1)
    t = hs.note(ax, 0.5, 0.5, r"Disposal floor $-\phi$", ha="right")
    assert t.get_fontsize() == pytest.approx(8 * hs.LATEX_SCALE)
    assert t.get_text() == r"$\text{Disposal floor }-\phi$"
    two = hs.note(ax, 0.5, 0.5, ["a", "b"], size=10, ha="left")
    assert two.get_text().count("\n") == 1 and two.get_fontsize() == pytest.approx(10 * hs.LATEX_SCALE)
    ax.figure.canvas.draw()


def test_tex_dashes():
    assert hs.tex("2020--2026") == r"$\text{2020" + "–" + "2026}$"
    assert hs.tex("a---b") == r"$\text{a" + "—" + "b}$"
    assert hs.tex("$x--y$") == "$x--y$"                  # math untouched


def test_legend_size_keeps_30pt_sample():
    _, ax = hs.figure(1, 1)
    a = hs.line(ax, [0, 1], [0, 1], 1)
    leg = hs.legend(ax, [a], ["x"], size=10)
    fs = leg.get_texts()[0].get_fontsize()
    assert fs == pytest.approx(10 * hs.LATEX_SCALE)
    assert leg.handlelength * fs == pytest.approx(30)


def test_legend_marker_only_short_sample():
    _, ax = hs.figure(1, 1)
    (p,) = ax.plot([0, 1], [0, 1], linestyle="none", marker="o")
    leg = hs.legend(ax, [p], ["points"])
    assert leg.handlelength * leg.get_texts()[0].get_fontsize() == pytest.approx(10)


def test_colorbar_geometry_and_style():
    fig, ax = hs.figure(1, 1, 600, 860)
    z = np.add.outer(np.arange(5.0), np.arange(5.0))
    cf = ax.contourf(z, levels=np.arange(0, 9))
    cb = hs.colorbar(ax, cf, label=r"Price $p_R$", ticks=[0, 4, 8])
    x, y, w, h = ax.get_position().bounds
    assert (x, y, w, h) == pytest.approx((0.13, 0.11, 0.7223, 0.815), abs=2e-4)   # MATLAB
    cx, cy, cw, ch = cb.ax.get_position().bounds
    assert cx == pytest.approx(x + w + 10.2 / 860, abs=1e-4) and cw == pytest.approx(21.4 / 860)
    assert not cb.ax.yaxis._major_tick_kw.get("gridOn", False)
    assert len(cb.ax.get_yticks(minor=True)) == 0
    hs.fit(fig)                                     # the bar follows the panel
    p = ax.get_position()
    assert cb.ax.get_position().x0 == pytest.approx(p.x1 + 10.2 / 860, abs=1e-6)
    assert cb.ax.get_position().height == pytest.approx(p.height)


def test_yyaxis_colors_and_fit_counts_twin():
    fig, ax = hs.figure(1, 1, 460)
    hs.line(ax, [0, 1], [0, 1], "data")
    ax2 = hs.yyaxis(ax)
    hs.line(ax2, [0, 1], [1, 0], 2)
    hs.finish(ax, None, "Left", zero=False)
    hs.finish(ax2, None, "A long right-hand label, units", zero=False)
    assert ax.yaxis.label.get_color() == hs.DATA and ax2.yaxis.label.get_color() == hs.SECOND
    assert ax2.spines["right"].get_edgecolor()[:3] == pytest.approx(hs.SECOND)
    assert not ax.spines["right"].get_visible()
    hs.fit(fig)
    r = fig.canvas.get_renderer()
    assert ax2.get_tightbbox(r).transformed(fig.transFigure.inverted()).x1 <= 1 + 1e-3
