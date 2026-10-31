# House style rules

The style comes from the mshipping replication scripts (`regen_wcbaseline.m`,
`regen_fig2_dataseries.m`, `regen_fig_confound.m`, `regen_fig_kanzig.m`). The Python
package (`src/housestyle`) and the MATLAB helpers (`matlab/toolbox`) apply most of
these rules for you. The rest are choices you make in each script.

Function names below are the MATLAB ones. In Python drop the prefix: `hs_band` is
`hs.band(ax, ...)`, `hs_figure(2)` is `hs.figure(2, 4)`.

## Pipeline

1. Compute in whatever language owns the analysis (Python, Stata, MATLAB). Write the
   plotted arrays, and only those, to a tidy CSV: one row per point, ISO dates
   `YYYY-MM-DD`.
2. One script per paper figure reads the CSV and draws it with the helpers, in Python
   or MATLAB.
3. The script ends with the export (`hs.export(fig, name)` or `hs_export(name)`) and
   reports what it wrote, so a batch run shows which figures finished.

## Figure and panels

- Figure: 1180 px wide, `30 + 285*rows` px tall, 13 pt axes font (`hs_figure`).
- Default grids: 1 x 4 (`hs_figure(1)`), 2 x 4 (`hs_figure(2)`). One wide panel:
  `hs_figure(1, 460)` with `hs_axes()`.
- Every panel: `hold on; grid on; box on` (`hs_axes`).
- No overall title (no `sgtitle`). The LaTeX caption carries the explanation.

## Marks

- Point estimate, baseline or model line: black, solid, `LineWidth` 2, drawn before
  its band.
- Band: patch in `[0 0.5 1]`, `FaceAlpha` 0.5, no edge (`hs_band`). The black line reads
  navy through it.
- One observed series on its own: MATLAB blue, `LineWidth` 1.5 (`hs_line(x, y, 'data')`).
- Several series: black solid, then orange `'--'`, green `'-.'`, purple with small
  dots (`hs_line(x, y, k)`). Line style as well as color tells series apart, so the
  figure survives grey print and colorblind readers. No dotted (`':'`) lines: they
  vanish in print. More than four series: use small multiples.
- Zero line: black `'--'`, only when 0 lies inside the y-limits, under the data
  (`hs_zero`).
- Shaded episode (a war, a recession): grey patch, `FaceAlpha` 0.15, under the data
  (`hs_shade`).
- Event marker: black dot, `MarkerSize` 4, label in 8 pt text (`hs_event`).
- Stacked bars (historical decompositions): `hs_colors().stack`, `EdgeColor` none, bar
  width 1, the total as a black line on top. The five colors pass a colorblind
  separation check; the yellow is faint on white, so keep the legend.

## Text

- Titles: short, plain, bold (MATLAB default), sentence case, no units, no LaTeX.
- Every panel carries a y label with units, LaTeX interpreter: `'Std'`, `'\%'`,
  `'USD/t, 2016 \$'`, `'$100\times\log$'`, `'Mt'`. Escape `% $ &`.
- Tick labels 10 pt. More than five y ticks: drop every other one, keeping 0
  (`hs_finish`).
- Legend in one panel only: `legend(..., 'Location', 'best', 'Interpreter', 'latex')`.
  For stacked bars, `'Location', 'southoutside', 'Orientation', 'horizontal'`.

## Axes

- Impulse responses: x is the horizon with 0 = impact, `xlabel('Months')`, so text
  that quotes h = 0, 6, 12 matches the axis. (The original mshipping figures count
  from 1.)
- Time axes: `datetime` x values, `xlim([min(x) max(x)])`, year tick labels.
- Right-hand y axes: avoid them where two panels would do. When a MATLAB figure needs
  one, `hs_export` switches export_fig to `-painters`, because the OpenGL route
  misdraws the right axis in R2026a.

## Output

- PNG at 300 dpi on a white background, cropped to the content (`hs_export`).
- Set the folder once per script or session with `hs_outdir`.
