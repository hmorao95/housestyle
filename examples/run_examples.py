"""Draw every example figure into images/ (the README gallery).

    py examples/run_examples.py [output folder]
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
try:
    import housestyle as hs
except ImportError:                                   # running from a source checkout
    sys.path.insert(0, str(HERE.parent / "src"))
    import housestyle as hs

import matplotlib

matplotlib.use("Agg")
sys.path.insert(0, str(HERE))

import example_compare  # noqa: E402
import example_decomposition  # noqa: E402
import example_irf_grid  # noqa: E402
import example_timeseries  # noqa: E402


def main() -> None:
    hs.outdir(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "images")
    for mod in (example_irf_grid, example_compare, example_timeseries, example_decomposition):
        print("wrote", mod.main())


if __name__ == "__main__":
    main()
