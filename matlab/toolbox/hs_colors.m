function c = hs_colors()
%HS_COLORS House palette. Line style as well as color tells series apart, so the
%   figures stay readable in grey print and for colorblind readers.
%   c.main    black       'k-'  LineWidth 2    point estimate, baseline, model
%   c.band    [0 0.5 1]   patch, FaceAlpha .5  credible or confidence band
%   c.data    MATLAB blue '-'   LineWidth 1.5  an observed series on its own
%   c.second  orange      '--'  LineWidth 1.8  second series
%   c.third   green       '-.'  LineWidth 1.8  third series
%   c.fourth  purple      '-o'  LineWidth 1.2  fourth series, small filled dots
%   c.grey    reference lines, shaded episodes (FaceAlpha .15)
%   c.stack   5 x 3 matrix for stacked bars: blue, orange, yellow, grey, green
%
%   See also hs_line, hs_band, hs_shade.
c.main   = [0 0 0];
c.band   = [0 0.5 1];
c.data   = [0 0.4470 0.7410];
c.second = [0.85 0.33 0.10];
c.third  = [0.10 0.60 0.10];
c.fourth = [0.49 0.18 0.56];
c.grey   = [0.5 0.5 0.5];
c.stack  = [0 0.5 1; 0.85 0.33 0.10; 0.93 0.69 0.13; 0.5 0.5 0.5; 0.10 0.60 0.10];
end
