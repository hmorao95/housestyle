function example_decomposition()
%EXAMPLE_DECOMPOSITION Historical decomposition as stacked bars with the total as a line.
%   Bars use hs_colors().stack; the legend sits below the axes in one row.
%   Writes example_decomposition.png to hs_outdir().
rng(3);
x = (datetime(2020, 1, 1):calmonths(1):datetime(2026, 6, 1))';
n = numel(x);
Y = filter(1, [1 -0.85], 0.25 * randn(n, 5));
total = sum(Y, 2);
labels = {'Supply', 'Fertilizer demand', 'Minerals demand', 'Oil-specific', 'Global activity'};
c = hs_colors();

hs_figure(1, 460); hs_axes();
b = bar(x, Y, 1, 'stacked', 'EdgeColor', 'none');
for s = 1:numel(b); b(s).FaceColor = c.stack(s, :); end
hl = hs_line(x, total, 1);
xlim([min(x) - days(20), max(x) + days(20)]);
up = sum(max(Y, 0), 2); dn = sum(min(Y, 0), 2);
ylim([min([dn; total]) - 0.25, max([up; total]) + 0.25]);
hs_zero();
legend([b hl], [labels, {'Total'}], 'Location', 'southoutside', ...
    'Orientation', 'horizontal', 'NumColumns', 6, 'Interpreter', 'latex');
hs_finish('Acid spread', 'Std');
hs_export('example_decomposition'); close(gcf);
end
