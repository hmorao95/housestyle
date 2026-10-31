function example_irf_grid()
%EXAMPLE_IRF_GRID Eight impulse responses in a 2 x 4 grid (regen_wcbaseline.m look).
%   Synthetic responses: a black median over a 68 percent band, h = 0 is impact.
%   Writes example_irf_grid.png to hs_outdir().
h = (0:24)';
names = {'Supply chain pressure', 'Shipping price', 'Global activity', 'Phosphate rock', ...
    'DAP price', 'TSP price', 'Urea price', 'Potash price'};
amp = [1 6 -0.8 4 3.5 3 2 2.5];
tau = [3 5 8 6 7 7 4 9];
hs_figure(2);
for k = 1:8
    med = amp(k) * (0.4 * exp(-h / tau(k)) + 0.6 * (h / tau(k)) .* exp(1 - h / tau(k)));
    se = abs(amp(k)) * (0.15 + 0.35 * sqrt(h / 24));
    if k == 1; ylab = 'Std'; else; ylab = '\%'; end
    if k > 4; xlab = 'Months'; else; xlab = ''; end
    hs_axes(2, 4, k);
    hs_irf(h, med, med - se, med + se, names{k}, ylab, xlab);
    xticks(0:6:24);
end
hs_export('example_irf_grid'); close(gcf);
end
