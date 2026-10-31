function run_examples(outdir)
%RUN_EXAMPLES Draw every example figure.
%   run_examples() writes the PNGs to hs_outdir() (default: the current folder).
%   run_examples(outdir) writes them to outdir and leaves hs_outdir as it was.
here = fileparts(mfilename('fullpath'));
addpath(fileparts(here));                       % the toolbox folder
key = 'housestyle_outdir';
old = getappdata(groot, key);
restore = onCleanup(@() reset_outdir(old));
if nargin >= 1; hs_outdir(outdir); end
example_irf_grid();
example_compare();
example_timeseries();
example_decomposition();
end

function reset_outdir(old)
if isempty(old); hs_outdir(''); else; hs_outdir(old); end
end
