function build_toolbox()
%BUILD_TOOLBOX Test housestyle, redraw the gallery, and package release/housestyle.mltbx.
%   Run from MATLAB in any folder: build_toolbox. Packaging needs R2023a or later.
%   Put export_fig on the path first so the gallery matches the house look.
root = fileparts(mfilename('fullpath'));
tbx = fullfile(root, 'toolbox');
addpath(tbx, fullfile(tbx, 'examples'));

% 1. tests
r = runtests(fullfile(root, 'tests'));
disp(table(r));
assertSuccess(r);

% 2. gallery for README.md
run_examples(fullfile(root, 'images'));

% 3. installable toolbox
opts = matlab.addons.toolbox.ToolboxOptions(tbx, 'f91fc781-933a-4805-873d-e436fc0392d4');
opts.ToolboxName = 'housestyle';
opts.ToolboxVersion = '1.0.0';
opts.AuthorName = 'Hugo Morão';
opts.Summary = 'Paper figures in the mshipping house style.';
opts.Description = ['Helpers for economics paper figures: black point estimate over a ' ...
    'translucent blue band, dashed zero line, bold plain titles, LaTeX axis labels, ' ...
    'line styles that survive grey print, and 300 dpi PNG export through export_fig.'];
opts.ToolboxMatlabPath = tbx;
opts.ToolboxImageFile = fullfile(root, 'images', 'example_irf_grid.png');
if ~isfolder(fullfile(root, 'release')); mkdir(fullfile(root, 'release')); end
opts.OutputFile = fullfile(root, 'release', 'housestyle.mltbx');
matlab.addons.toolbox.packageToolbox(opts);
fprintf('wrote %s\n', opts.OutputFile);
end
