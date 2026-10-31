function l = hs_zero(ax)
%HS_ZERO Dashed black zero line, only when 0 lies strictly inside the y-limits.
%   l = hs_zero() draws it on the current axes and sends it to the bottom, so data
%   and bands sit on top. Returns [] when no line is drawn.
%   l = hs_zero(ax) uses axes ax.
%
%   Call it after xlim is set: the line spans the x-limits at call time.
%
%   See also hs_irf.
if nargin < 1 || isempty(ax); ax = gca; end
l = [];
pl = get(ax, 'YLim');
if ~ismember(0, pl) && ~(pl(1) > 0 || pl(2) < 0)
    l = line(ax, get(ax, 'XLim'), [0 0], 'Color', 'k', 'LineStyle', '--', ...
        'HandleVisibility', 'off');
    uistack(l, 'bottom');
end
end
