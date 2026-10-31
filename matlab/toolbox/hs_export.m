function out = hs_export(file, f, varargin)
%HS_EXPORT Save a figure on a white background as a 300 dpi PNG.
%   hs_export('fig1') writes fig1.png to hs_outdir() (default: the current folder).
%   hs_export('figs/fig1.png') or a full path writes exactly there.
%   hs_export(file, f) exports figure f (default gcf).
%   hs_export(file, f, opts...) passes options to export_fig, e.g. '-r600' or '-pdf'.
%   out = hs_export(...) returns the path written.
%
%   With export_fig on the path (github.com/altmany/export_fig) the output matches
%   the mshipping figures. Without it, hs_export falls back to exportgraphics at the
%   same resolution and warns once per session.
%   A figure with a right-hand y axis (yyaxis) exports with -painters, because the
%   OpenGL route misdraws the right axis in R2026a.
%
%   See also hs_outdir, hs_figure.
persistent warned
if nargin < 2 || isempty(f); f = gcf; end
file = char(file);
[folder, stem, ext] = fileparts(file);
if isempty(ext); ext = '.png'; end
if isempty(folder); folder = hs_outdir(); end
if ~isfolder(folder); mkdir(folder); end
out = fullfile(folder, [stem ext]);
set(f, 'Color', 'w');
opts = cellfun(@char, varargin, 'UniformOutput', false);
res = regexp(opts, '^-r(\d+)$', 'tokens', 'once');
hasres = ~cellfun(@isempty, res);
if exist('export_fig', 'file') == 2
    if ~any(hasres); opts = [{'-r300'}, opts]; end
    renderers = {'-painters', '-opengl', '-zbuffer', '-vector'};
    if has_right_axis(f) && ~any(ismember(lower(opts), renderers))
        opts = [opts, {'-painters'}];
    end
    export_fig(f, out, opts{:});
else
    if isempty(warned)
        warning('housestyle:noExportFig', ['export_fig is not on the path; using ' ...
            'exportgraphics. Add export_fig to match the house look exactly.']);
        warned = true;
    end
    dpi = 300;
    if any(hasres); dpi = str2double(res{find(hasres, 1)}{1}); end
    exportgraphics(f, out, 'Resolution', dpi, 'BackgroundColor', 'white');
end
fprintf('wrote %s\n', out);
end

function tf = has_right_axis(f)
tf = false;
ax = findall(f, 'Type', 'axes');
for k = 1:numel(ax)
    if numel(ax(k).YAxis) > 1; tf = true; return; end
end
end
