function tests = test_housestyle
%TEST_HOUSESTYLE Unit tests for the housestyle helpers. Run: runtests('tests')
tests = functiontests(localfunctions);
end

function setupOnce(tc)
root = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(root, 'toolbox'));
tc.TestData.tmp = tempname;
mkdir(tc.TestData.tmp);
tc.TestData.oldOut = getappdata(groot, 'housestyle_outdir');
end

function teardownOnce(tc)
close all force;
if isempty(tc.TestData.oldOut); hs_outdir(''); else; hs_outdir(tc.TestData.oldOut); end
rmdir(tc.TestData.tmp, 's');
end

function teardown(~)
close all force;
end

% ---- figure and panels -------------------------------------------------------

function testFigureSize(tc)
f = hs_figure(2);
tc.verifyEqual(f.Position(3:4), [1180 600]);
f = hs_figure(1, 460, 860);
tc.verifyEqual(f.Position(3:4), [860 460]);
end

function testAxesSettings(tc)
hs_figure(); ax = hs_axes(1, 2, 2);
tc.verifyTrue(ishold(ax));
tc.verifyEqual(char(ax.XGrid), 'on');
tc.verifyEqual(char(ax.Box), 'on');
end

function testFinishLabels(tc)
hs_figure(); hs_axes(); plot(1:3);
hs_finish('Oil', '\%', 'Months');
ax = gca;
tc.verifyEqual(ax.Title.String, 'Oil');
tc.verifyEqual(ax.YLabel.Interpreter, 'latex');
tc.verifyEqual(ax.XLabel.String, 'Months');
tc.verifyEqual(ax.XAxis.FontSize, 10);
tc.verifyEqual(ax.YAxis.FontSize, 10);
end

function testTickThinningKeepsZero(tc)
hs_figure(); hs_axes(); plot(1:3, [-3 0 3]); ylim([-3 3]); yticks(-3:3);
hs_finish('', 'Std');
ax = gca;
tc.verifyEqual(ax.YTick, [-2 0 2]);
end

function testTickThinningManualLabels(tc)
hs_figure(); hs_axes(); plot(1:3, [1 4 7]); ylim([1 7]);
yticks(1:7); yticklabels({'a', 'b', 'c', 'd', 'e', 'f', 'g'});
hs_finish();
ax = gca;
tc.verifyEqual(ax.YTick, [1 3 5 7]);
tc.verifyEqual(ax.YTickLabel(:)', {'a', 'c', 'e', 'g'});
end

% ---- marks ---------------------------------------------------------------------

function testZeroLineInside(tc)
hs_figure(); ax = hs_axes(); plot(1:3, [-1 0.5 1]); ylim([-1 1]);
l = hs_zero();
tc.verifyEqual(l.YData, [0 0]);
tc.verifyEqual(char(l.LineStyle), '--');
ch = allchild(ax);                                % includes legend-hidden objects
tc.verifyEqual(ch(end), l);                       % drawn under the data
end

function testZeroLineOutside(tc)
hs_figure(); hs_axes(); plot(1:3, [1 2 3]); ylim([1 3]);
tc.verifyEmpty(hs_zero());
end

function testIrfPanel(tc)
hs_figure(); ax = hs_axes();
h = (0:12)'; m = exp(-h / 4);
[hl, hb] = hs_irf(h, m, m - 0.3, m + 0.3, 'Oil', 'Std', 'Months');
tc.verifyEqual(ax.XLim, [0 12]);
tc.verifyEqual(hl.Color, [0 0 0]);
tc.verifyEqual(hl.LineWidth, 2);
tc.verifyEqual(hb.FaceAlpha, 0.5);
tc.verifyEqual(hb.FaceColor, [0 0.5 1]);
tc.verifyNumElements(findall(ax, 'Type', 'line', 'LineStyle', '--'), 1);
end

function testIrfWithoutBand(tc)
hs_figure(); hs_axes();
[~, hb] = hs_irf(0:6, ones(1, 7));
tc.verifyEmpty(hb);
end

function testLineStyles(tc)
c = hs_colors();
hs_figure(); hs_axes();
h1 = hs_line(1:3, 1:3, 1);
h2 = hs_line(1:3, 1:3, 'second');
h3 = hs_line(1:3, 1:3, 3);
h4 = hs_line(1:3, 1:3, 4);
hd = hs_line(1:3, 1:3, 'data', 'DisplayName', 'Observed');
tc.verifyEqual(h1.Color, c.main);  tc.verifyEqual(char(h1.LineStyle), '-');
tc.verifyEqual(h1.LineWidth, 2);
tc.verifyEqual(h2.Color, c.second, 'AbsTol', 1e-12); tc.verifyEqual(char(h2.LineStyle), '--');
tc.verifyEqual(h3.Color, c.third, 'AbsTol', 1e-12);  tc.verifyEqual(char(h3.LineStyle), '-.');
tc.verifyEqual(char(h4.Marker), 'o');
tc.verifyEqual(hd.Color, c.data, 'AbsTol', 1e-12);
tc.verifyEqual(hd.DisplayName, 'Observed');
styles = {h1.LineStyle, h2.LineStyle, h3.LineStyle, h4.LineStyle, hd.LineStyle};
tc.verifyFalse(any(strcmp(cellfun(@char, styles, 'UniformOutput', false), ':')));
end

function testLineErrors(tc)
hs_figure(); hs_axes();
tc.verifyError(@() hs_line(1:3, 1:3, 5), 'hs_line:tooMany');
tc.verifyError(@() hs_line(1:3, 1:3, 'fifth'), 'hs_line:role');
end

function testBandDatetime(tc)
hs_figure(); hs_axes();
x = datetime(2020, 1:12, 1); y = sin(1:12);
plot(x, y, 'k-', 'LineWidth', 2);
p = hs_band(x, y - 0.2, y + 0.2);
tc.verifyEqual(p.FaceAlpha, 0.5);
end

function testShadeAndEvent(tc)
hs_figure(); ax = hs_axes();
x = datetime(2020, 1, 1) + calmonths(0:23); y = sin(1:24);
plot(x, y);
yl = ylim;
p = hs_shade(datetime(2021, 1, 1), datetime(2021, 6, 1));
tc.verifyEqual(ylim, yl);
tc.verifyEqual(p.FaceAlpha, 0.15);
ch = allchild(ax);
tc.verifyEqual(ch(end), p);
[hp, ht] = hs_event(x(5), y(5), 'Event');
tc.verifyEqual(char(hp.Marker), 'o');
tc.verifyEqual(ht.FontSize, 8);
[~, ht] = hs_event(x(5), -0.5, 'Below');
tc.verifyEqual(char(ht.VerticalAlignment), 'top');
end

function testColors(tc)
c = hs_colors();
tc.verifyEqual(fieldnames(c)', {'main', 'band', 'data', 'second', 'third', 'fourth', 'grey', 'stack'});
tc.verifySize(c.stack, [5 3]);
end

% ---- output --------------------------------------------------------------------

function testOutdir(tc)
old = pwd; restore = onCleanup(@() cd(old));
cd(tc.TestData.tmp);
d = hs_outdir('sub');
tc.verifyEqual(d, fullfile(tc.TestData.tmp, 'sub'));
tc.verifyTrue(isfolder(d));
cd(old);
tc.verifyEqual(hs_outdir(), d);                 % a later cd does not move it
tc.verifyEqual(hs_outdir(''), pwd);
tc.verifyEqual(hs_outdir(), pwd);
end

function testExportToOutdir(tc)
hs_outdir(tc.TestData.tmp);
hs_figure(); hs_axes(); plot(1:3);
out = hs_export('t1');
tc.verifyEqual(out, fullfile(tc.TestData.tmp, 't1.png'));
tc.verifyTrue(isfile(out));
info = imfinfo(out);
tc.verifyGreaterThan(info.Width, 2000);         % 1180 px at 300 dpi
end

function testExportResolutionOption(tc)
hs_figure(); hs_axes(); plot(1:3);
a = imfinfo(hs_export(fullfile(tc.TestData.tmp, 'r300.png')));
b = imfinfo(hs_export(fullfile(tc.TestData.tmp, 'r150.png'), gcf, '-r150'));
tc.verifyLessThan(b.Width, 0.6 * a.Width);
end

function testExportRightAxis(tc)
hs_figure(1, 460); hs_axes();
yyaxis left; plot(1:10, rand(1, 10));
yyaxis right; plot(1:10, 100 * rand(1, 10));
hs_finish('Two axes', 'Mt');
out = hs_export(fullfile(tc.TestData.tmp, 'yy.png'));
tc.verifyTrue(isfile(out));
end

function testExportFallback(tc)
p = fileparts(which('export_fig'));
if ~isempty(p)
    rmpath(p);
    tc.addTeardown(@() addpath(p));
end
hs_figure(); hs_axes(); plot(1:3);
w = warning('off', 'housestyle:noExportFig');
tc.addTeardown(@() warning(w));
out = hs_export(fullfile(tc.TestData.tmp, 'fallback.png'));
tc.verifyTrue(isfile(out));
tc.verifyGreaterThan(imfinfo(out).Width, 2000);
end
