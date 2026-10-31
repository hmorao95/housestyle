function example_compare()
%EXAMPLE_COMPARE Baseline with band against two alternatives (regen_fig_confound.m look).
%   Built from the pieces rather than hs_irf, to show the drawing order: baseline,
%   band, alternatives, then the zero line and labels. Legend in one panel only.
%   Writes example_compare.png to hs_outdir().
h = (0:24)';
names = {'Oil price', 'Copper price', 'Potash price', 'Acid spread'};
amp = [3 -1.5 2 4];
tau = [4 9 6 7];
hs_figure(1);
for k = 1:4
    base = amp(k) * (h / tau(k)) .* exp(1 - h / tau(k));
    se = abs(amp(k)) * (0.2 + 0.3 * sqrt(h / 24));
    hs_axes(1, 4, k);
    h1 = hs_line(h, base, 1);
    hs_band(h, base - se, base + se);
    h2 = hs_line(h, 0.8 * base, 2);
    h3 = hs_line(h, 1.15 * base .* exp(-h / 40), 3);
    xlim([0 24]); xticks(0:6:24);
    hs_zero();
    hs_finish(names{k}, '\%', 'Months');
    if k == 4
        legend([h1 h2 h3], {'Baseline', 'More lags', 'Shorter sample'}, ...
            'Location', 'best', 'Interpreter', 'latex');
    end
end
hs_export('example_compare'); close(gcf);
end
