function d = hs_outdir(d)
%HS_OUTDIR Get or set the folder that hs_export writes bare file names to.
%   hs_outdir('figures') sets it and creates the folder if needed. A relative path
%   resolves against the current folder now, so a later cd does not move it.
%   d = hs_outdir() returns it. The default is the current folder.
%   hs_outdir('') resets it to the default.
%   The setting lasts for the MATLAB session and survives clear all.
%
%   See also hs_export.
key = 'housestyle_outdir';
if nargin >= 1
    d = char(d);
    if isempty(d)
        if isappdata(groot, key); rmappdata(groot, key); end
        d = pwd;
        return
    end
    if isempty(regexp(d, '^([A-Za-z]:[\\/]|[\\/])', 'once')); d = fullfile(pwd, d); end
    if ~isfolder(d); mkdir(d); end
    setappdata(groot, key, d);
    return
end
d = getappdata(groot, key);
if isempty(d); d = pwd; end
end
