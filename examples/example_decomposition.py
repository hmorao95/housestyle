"""Historical decomposition as stacked bars with the total as a black line.

Bars use hs.STACK; the legend sits below the axes in one row.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import housestyle as hs

LABELS = ["Supply", "Fertilizer demand", "Minerals demand", "Oil-specific", "Global activity"]


def main() -> Path:
    rng = np.random.default_rng(3)
    x = np.arange("2020-01", "2026-07", dtype="datetime64[M]").astype("datetime64[D]")
    e = 0.25 * rng.standard_normal((x.size, 5))
    Y = np.zeros_like(e)
    for i in range(x.size):                       # AR(1) contributions
        Y[i] = e[i] + (0.85 * Y[i - 1] if i else 0)
    total = Y.sum(axis=1)

    fig, ax = hs.figure(1, 1, 460)
    bars = hs.bars(ax, x, Y)
    hl = hs.line(ax, x, total, 1)
    ax.set_xlim(x[0] - np.timedelta64(20, "D"), x[-1] + np.timedelta64(20, "D"))
    up, dn = np.clip(Y, 0, None).sum(1), np.clip(Y, None, 0).sum(1)
    ax.set_ylim(min(dn.min(), total.min()) - 0.25, max(up.max(), total.max()) + 0.25)
    hs.finish(ax, "Acid spread", "Std")
    hs.legend(ax, [*bars, hl], [*LABELS, "Total"], outside="south")
    return hs.export(fig, "example_decomposition", close=True)


if __name__ == "__main__":
    print("wrote", main())
