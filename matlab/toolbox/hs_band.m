function p = hs_band(x, lo, hi, color, alpha)
%HS_BAND Credible or confidence band as a translucent patch, house style.
%   p = hs_band(x, lo, hi) shades [lo, hi] over x in blue [0 0.5 1], alpha 0.5,
%   with no edge, and keeps it out of the legend.
%   p = hs_band(x, lo, hi, color, alpha) sets the color and transparency.
%
%   Draw the point estimate first, plot(x, med, 'k-', 'LineWidth', 2), then the
%   band: the black line then reads navy through it. x may be datetime.
%
%   See also hs_irf, hs_colors.
if nargin < 4 || isempty(color); color = [0 0.5 1]; end
if nargin < 5 || isempty(alpha); alpha = .5; end
x = x(:); lo = lo(:); hi = hi(:);
p = patch([x; flipud(x)], [hi; flipud(lo)], 1, 'FaceColor', color, ...
    'EdgeColor', 'none', 'FaceAlpha', alpha, 'HandleVisibility', 'off');
end
