function example_timeseries()
%EXAMPLE_TIMESERIES Monthly series with a shaded episode and event markers.
%   Left: one observed series in MATLAB blue. Right: two series told apart by line
%   style and color, with the shaded episode listed in the legend.
%   Writes example_timeseries.png to hs_outdir().
rng(7);
t = (datetime(2015, 1, 1):calmonths(1):datetime(2026, 6, 1))';
n = numel(t);
ip = find(t == datetime(2022, 4, 1));
spike = 120 * exp(-((1:n)' - ip) .^ 2 / (2 * 4 ^ 2));
p = 100 + cumsum(3 * randn(n, 1)) + spike;
q = 0.8 * p + 15 + cumsum(1.5 * randn(n, 1));
war = [datetime(2022, 2, 24), datetime(2022, 12, 31)];

hs_figure(1, 380);
hs_axes(1, 2, 1);
hs_line(t, p, 'data');
xlim([min(t) max(t)]);
ylim([80 260]);                                 % headroom for the event label
hs_shade(war(1), war(2));
hs_event(t(ip), p(ip), 'Peak');
hs_event(datetime(2019, 6, 1), p(t == datetime(2019, 6, 1)), {'Policy'; 'change'});
hs_finish('Real price', 'USD/t, 2016 \$');

hs_axes(1, 2, 2);
h1 = hs_line(t, p, 1);
h2 = hs_line(t, q, 2);
xlim([min(t) max(t)]);
s = hs_shade(war(1), war(2));
set(s, 'HandleVisibility', 'on');
hs_finish('Two series', 'USD/t, 2016 \$');
legend([h1 h2 s], {'Spot', 'Contract', 'War months'}, 'Location', 'northwest', ...
    'Interpreter', 'latex');
hs_export('example_timeseries'); close(gcf);
end
