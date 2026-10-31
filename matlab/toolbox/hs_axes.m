function ax = hs_axes(varargin)
%HS_AXES Start a panel in the house style: subplot, then hold, grid and box on.
%   ax = hs_axes(rows, cols, k) is subplot(rows, cols, k) plus the house settings.
%   ax = hs_axes() applies the settings to the current axes (one-panel figures).
%
%   See also hs_figure, hs_finish.
if nargin > 0; subplot(varargin{:}); end
hold on; grid on; box on
ax = gca;
end
