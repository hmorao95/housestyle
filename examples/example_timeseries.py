"""Monthly series with a shaded episode and event markers.

Left: one observed series in MATLAB blue. Right: two series told apart by line style
and color, with the shaded episode listed in the legend.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import housestyle as hs


def main() -> Path:
    rng = np.random.default_rng(7)
    t = np.arange("2015-01", "2026-07", dtype="datetime64[M]").astype("datetime64[D]")
    n = t.size
    ip = int(np.flatnonzero(t == np.datetime64("2022-04-01"))[0])
    spike = 120 * np.exp(-((np.arange(n) - ip) ** 2) / (2 * 4 ** 2))
    p = 100 + np.cumsum(3 * rng.standard_normal(n)) + spike
    q = 0.8 * p + 15 + np.cumsum(1.5 * rng.standard_normal(n))
    war = (np.datetime64("2022-02-24"), np.datetime64("2022-12-31"))
    ipol = int(np.flatnonzero(t == np.datetime64("2019-06-01"))[0])

    fig, (left, right) = hs.figure(1, 2, 380)
    hs.line(left, t, p, "data")
    left.set_xlim(t[0], t[-1])
    left.set_ylim(np.floor(p.min() / 20) * 20, np.ceil(p.max() * 1.1 / 20) * 20)  # headroom
    hs.shade(left, *war)
    hs.event(left, t[ip], p[ip], "Peak")
    hs.event(left, t[ipol], p[ipol], ["Policy", "change"])
    hs.finish(left, "Real price", "USD/t, 2016 $")

    h1 = hs.line(right, t, p, 1)
    h2 = hs.line(right, t, q, 2)
    right.set_xlim(t[0], t[-1])
    s = hs.shade(right, *war, label="War months")
    hs.finish(right, "Two series", "USD/t, 2016 $")
    hs.legend(right, [h1, h2, s], ["Spot", "Contract", "War months"], loc="upper left")
    return hs.export(fig, "example_timeseries", close=True)


if __name__ == "__main__":
    print("wrote", main())
