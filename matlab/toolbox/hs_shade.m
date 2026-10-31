function p = hs_shade(x0, x1, color, alpha)
%HS_SHADE Grey shaded episode from x0 to x1, behind the data.
%   p = hs_shade(x0, x1) shades [x0, x1] over the full y range in grey, FaceAlpha
%   0.15, and sends it to the bottom. x0 and x1 may be datetime.
%   p = hs_shade(x0, x1, color, alpha) sets the color and transparency.
%
%   Call it after the data are drawn. It freezes the current y-limits so the shading
%   still fills the panel. To list it in a legend:
%     set(p, 'HandleVisibility', 'on', 'DisplayName', 'War months')
%
%   See also hs_event, hs_colors.
if nargin < 3 || isempty(color); c = hs_colors(); color = c.grey; end
if nargin < 4 || isempty(alpha); alpha = .15; end
ax = gca; yl = ylim(ax);
p = patch(ax, [x0 x1 x1 x0], yl([1 1 2 2]), color, 'FaceAlpha', alpha, ...
    'EdgeColor', 'none', 'HandleVisibility', 'off');
uistack(p, 'bottom');
ylim(ax, yl);
end
