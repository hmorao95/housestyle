"""Baseline with band against two alternatives (regen_fig_confound.m look).

Built from the pieces rather than hs.irf, to show the drawing order: baseline, band,
alternatives, then finish() for the zero line and labels. Legend in one panel only.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import housestyle as hs

NAMES = ["Oil price", "Copper price", "Potash price", "Acid spread"]
AMP = np.array([3, -1.5, 2, 4])
TAU = np.array([4, 9, 6, 7])


def main() -> Path:
    h = np.arange(25)
    fig, axes = hs.figure(1, 4)
    for k, ax in enumerate(axes):
        base = AMP[k] * (h / TAU[k]) * np.exp(1 - h / TAU[k])
        se = abs(AMP[k]) * (0.2 + 0.3 * np.sqrt(h / 24))
        h1 = hs.line(ax, h, base, 1)
        hs.band(ax, h, base - se, base + se)
        h2 = hs.line(ax, h, 0.8 * base, 2)
        h3 = hs.line(ax, h, 1.15 * base * np.exp(-h / 40), 3)
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 25, 6))
        hs.finish(ax, NAMES[k], "%", "Months")
        if k == 3:
            hs.legend(ax, [h1, h2, h3], ["Baseline", "More lags", "Shorter sample"])
    return hs.export(fig, "example_compare", close=True)


if __name__ == "__main__":
    print("wrote", main())
