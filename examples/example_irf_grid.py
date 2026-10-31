"""Eight impulse responses in a 2 x 4 grid (regen_wcbaseline.m look).

Synthetic responses: a black median over a 68 percent band, h = 0 is impact.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import housestyle as hs

NAMES = ["Supply chain pressure", "Shipping price", "Global activity", "Phosphate rock",
         "DAP price", "TSP price", "Urea price", "Potash price"]
AMP = np.array([1, 6, -0.8, 4, 3.5, 3, 2, 2.5])
TAU = np.array([3, 5, 8, 6, 7, 7, 4, 9])


def main() -> Path:
    h = np.arange(25)
    fig, axes = hs.figure(2, 4)
    for k, ax in enumerate(axes.flat):
        med = AMP[k] * (0.4 * np.exp(-h / TAU[k]) + 0.6 * (h / TAU[k]) * np.exp(1 - h / TAU[k]))
        se = abs(AMP[k]) * (0.15 + 0.35 * np.sqrt(h / 24))
        ax.set_xticks(range(0, 25, 6))
        hs.irf(ax, h, med, med - se, med + se, NAMES[k],
               ylabel="Std" if k == 0 else "%", xlabel="Months" if k >= 4 else None)
    return hs.export(fig, "example_irf_grid", close=True)


if __name__ == "__main__":
    print("wrote", main())
