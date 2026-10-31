function [hl, hb] = hs_irf(h, med, lo, hi, ttl, ylab, xlab)
%HS_IRF One impulse-response panel in the house style, on the current axes.
%   hs_irf(h, med, lo, hi) draws the median as a black line (LineWidth 2), the band
%   [lo, hi] as a translucent blue patch over it, sets xlim to the horizon range and
%   adds the dashed zero line. Pass lo = [] and hi = [] for no band.
%   hs_irf(h, med, lo, hi, ttl, ylab, xlab) also sets the title and labels.
%   [hl, hb] = hs_irf(...) returns the line and band handles (hl for a legend).
%
%   Convention: h = 0 is impact, so text that quotes h = 0, 6, 12 matches the axis.
%
%   Example
%     hs_figure(2);
%     for k = 1:8
%         hs_axes(2, 4, k);
%         hs_irf(0:24, med(:, k), lo(:, k), hi(:, k), names{k}, 'Std', 'Months');
%     end
%     hs_export('irf_baseline');
%
%   See also hs_band, hs_zero, hs_finish, hs_line.
if nargin < 3; lo = []; end
if nargin < 4; hi = []; end
if nargin < 5; ttl = ''; end
if nargin < 6; ylab = ''; end
if nargin < 7; xlab = ''; end
hold on; grid on; box on
h = h(:);
hl = plot(h, med(:), 'k-', 'LineWidth', 2);
hb = [];
if ~isempty(lo) && ~isempty(hi); hb = hs_band(h, lo, hi); end
xlim([min(h) max(h)]);
hs_zero();
hs_finish(ttl, ylab, xlab);
end
