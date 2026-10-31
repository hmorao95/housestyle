function f = hs_figure(rows, height, width)
%HS_FIGURE New figure in the house style.
%   f = hs_figure(rows) opens a figure 1180 px wide and 30 + 285*rows px tall,
%   with a 13 pt default axes font and a white background.
%   f = hs_figure(rows, height) sets the height in pixels.
%   f = hs_figure(rows, height, width) also sets the width in pixels.
%
%   Typical grids: hs_figure(1) for 1 x 4 panels, hs_figure(2) for 2 x 4,
%   hs_figure(1, 460) for one wide panel.
%
%   See also hs_axes, hs_finish, hs_export.
if nargin < 1 || isempty(rows); rows = 1; end
if nargin < 2 || isempty(height); height = 30 + 285 * rows; end
if nargin < 3 || isempty(width); width = 1180; end
f = figure('Position', [100 100 width height], 'PaperPositionMode', 'Auto', ...
    'DefaultAxesFontSize', 13, 'Color', 'w');
end
