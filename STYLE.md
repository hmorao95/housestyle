# House style rules

The style comes from the mshipping replication scripts (`regen_wcbaseline.m` and its
siblings). The `housestyle` package applies most of these rules for you; the rest are
choices you make in each figure script.

## Pipeline

1. The compute script writes the plotted arrays, and only those, to a tidy CSV: one
   row per point, ISO dates `YYYY-MM-DD`.
2. One figure script per paper figure reads the CSV and draws it with `housestyle`.
3. The script ends with `hs.export(fig, "<paper file name>")` and returns or prints
   the path written, so a batch run shows which figures finished.

## Figure and panels

- Figure: 1180 MATLAB pixels wide, `30 + 285*rows` tall (`hs.figure(rows, cols)`).
- Default grids: `hs.figure(1, 4)` and `hs.figure(2, 4)`. One wide panel:
  `hs.figure(1, 1, 460)`.
- Every panel: grid on, box on, inward ticks on all four sides (set by `hs.figure`).
- No overall title. The LaTeX caption carries the explanation.

## Marks

- Point estimate, baseline or model line: black, solid, 2 pt (`hs.line(ax, x, y, 1)`),
  drawn before its band.
- Band: `[0 0.5 1]` at alpha 0.5, no edge (`hs.band`). The black line reads navy
  through it. `hs.irf` draws line, band, zero line and labels in one call.
- One observed series on its own: MATLAB blue, 1.5 pt (`hs.line(ax, x, y, "data")`).
- Several series: black solid, then orange `--`, green `-.`, purple with small dots
  (`hs.line(ax, x, y, k)`). Line style as well as color tells series apart, so the
  figure survives grey print and colorblind readers. No dotted lines: they vanish in
  print. More than four series: use small multiples.
- Zero line: black `--`, 0.5 pt, only when 0 lies inside the y-limits, under the data
  (`hs.zero`, or `hs.finish` by default).
- Shaded episode (a war, a recession): grey at alpha 0.15, under the data (`hs.shade`).
- Event marker: black dot, size 4, label in 8 pt text (`hs.event`).
- Stacked bars (historical decompositions): `hs.bars` with `hs.STACK`, touching, no
  edges, the total as a black line on top. The five colors pass a colorblind
  separation check; the yellow is faint on white, so keep the legend.

## Text

- Titles: short, plain, bold, sentence case, no units, no LaTeX.
- Every panel carries a y label with units, drawn as LaTeX text: `"Std"`, `"%"`,
  `"USD/t, 2016 $"`, `"$100\times\log$"`, `"Mt"` (`hs.finish`).
- Tick labels 10 pt, written as MATLAB writes numbers. More than five y ticks: drop
  every other one, keeping 0 (`hs.finish`).
- Legend in one panel only, `loc="best"` (`hs.legend`). For stacked bars,
  `outside="south"`.

## Axes

- Impulse responses: x is the horizon with 0 = impact, x label `"Months"`, so text
  that quotes h = 0, 6, 12 matches the axis. (The original mshipping figures count
  from 1.)
- Time axes: dates on x, `ax.set_xlim(first, last)`, year tick labels (`hs.finish`
  or `hs.years`).
- Right-hand y axes: avoid them where two panels would do.

## Output

- PNG at 300 dpi on a white background, cropped to the content (`hs.export`).
- Set the folder once per script or session with `hs.outdir`.
