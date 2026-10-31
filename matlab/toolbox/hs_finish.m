function hs_finish(ttl, ylab, xlab)
%HS_FINISH Title, labels and tick fonts for the current panel, house style.
%   hs_finish(ttl, ylab, xlab)
%     ttl   plain bold title (not LaTeX), sentence case, no units; '' for none
%     ylab  y label with units, LaTeX interpreter: 'Std', '\%', 'USD/t, 2016 \$'
%     xlab  x label, LaTeX interpreter, e.g. 'Months'; optional
%   Tick labels are set to 10 pt. With more than 5 y ticks, every other tick is
%   dropped, keeping 0 when it is a tick; manual tick labels are thinned with them.
%
%   See also hs_axes, hs_irf.
if nargin >= 1 && ~isempty(ttl); title(ttl); end
if nargin >= 2 && ~isempty(ylab); tl = ylabel(ylab); set(tl, 'Interpreter', 'latex'); end
if nargin >= 3 && ~isempty(xlab); tl = xlabel(xlab); set(tl, 'Interpreter', 'latex'); end
ax = gca; ax.XAxis.FontSize = 10;
for k = 1:numel(ax.YAxis); ax.YAxis(k).FontSize = 10; end
if numel(ax.YTick) > 5
    t = ax.YTick; z = find(abs(t) < 1e-12, 1);
    if isempty(z); keep = 1:2:numel(t); else; keep = mod(z - 1, 2) + 1:2:numel(t); end
    manual = strcmp(ax.YTickLabelMode, 'manual'); lab = ax.YTickLabel;
    ax.YTick = t(keep);
    if manual && numel(lab) == numel(t); ax.YTickLabel = lab(keep); end
end
end
