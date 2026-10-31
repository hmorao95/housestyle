function hl = hs_line(x, y, k, varargin)
%HS_LINE Plot a series in the house order, so line style and color both identify it.
%   hl = hs_line(x, y, k) plots series k on the current axes:
%     1         black solid, LineWidth 2         baseline, point estimate, model
%     2         orange dashed, LineWidth 1.8
%     3         green dash-dot, LineWidth 1.8
%     4         purple solid with small filled dots, LineWidth 1.2
%     'data'    MATLAB blue solid, LineWidth 1.5  an observed series on its own
%   The names 'main', 'second', 'third' and 'fourth' work in place of 1 to 4.
%   hl = hs_line(..., Name, Value) passes options to plot, e.g. 'DisplayName'.
%
%   There is no fifth style and no dotted style (dots vanish in print). For more
%   series, use small multiples.
%
%   See also hs_colors, hs_irf.
c = hs_colors();
if nargin < 3 || isempty(k); k = 1; end
if isstring(k) || ischar(k)
    names = {'main', 'second', 'third', 'fourth'};
    role = lower(char(k));
    if strcmp(role, 'data')
        hl = plot(x, y, '-', 'Color', c.data, 'LineWidth', 1.5, varargin{:});
        return
    end
    k = find(strcmp(role, names), 1);
    if isempty(k)
        error('hs_line:role', 'Unknown series ''%s''. Use 1 to 4, or ''data''.', role);
    end
end
switch k
    case 1
        sty = {'-', 'Color', c.main, 'LineWidth', 2};
    case 2
        sty = {'--', 'Color', c.second, 'LineWidth', 1.8};
    case 3
        sty = {'-.', 'Color', c.third, 'LineWidth', 1.8};
    case 4
        sty = {'-', 'Color', c.fourth, 'LineWidth', 1.2, 'Marker', 'o', ...
            'MarkerSize', 3.5, 'MarkerFaceColor', c.fourth};
    otherwise
        error('hs_line:tooMany', ...
            'The house style has four line series. Use small multiples for more.');
end
hl = plot(x, y, sty{:}, varargin{:});
end
