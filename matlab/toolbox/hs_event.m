function [hp, ht] = hs_event(x, y, label, align)
%HS_EVENT Black dot at (x, y) with a short 8 pt label (regen_fig_kanzig.m style).
%   [hp, ht] = hs_event(x, y, label) puts the label above the dot when y >= 0 and
%   below it otherwise. label may be a cell array of lines, for example
%   {'Russia''s invasion'; 'of Ukraine'}. Pass '' for a dot with no label.
%   hs_event(x, y, label, align) sets the horizontal alignment of the label:
%   'center' (default), 'left' or 'right'.
%
%   Call it after the y-limits are final: the label offset is 3 percent of the
%   y range. Leave headroom above a peak, e.g. ylim([lo hi + 0.1*(hi - lo)]),
%   or the label runs into the title.
%
%   See also hs_shade.
if nargin < 3; label = ''; end
if nargin < 4 || isempty(align); align = 'center'; end
hp = plot(x, y, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 4, 'HandleVisibility', 'off');
ht = [];
if isempty(label); return; end
dy = 0.03 * diff(ylim);
if y >= 0
    ht = text(x, y + dy, label, 'FontSize', 8, 'HorizontalAlignment', align, ...
        'VerticalAlignment', 'bottom');
else
    ht = text(x, y - dy, label, 'FontSize', 8, 'HorizontalAlignment', align, ...
        'VerticalAlignment', 'top');
end
end
