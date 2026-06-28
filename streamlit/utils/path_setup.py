"""
Path Setup Utility
Project: Customer Churn Intelligence Platform

Ensures the project root is on sys.path so that
imports from the `src` package work correctly when
Streamlit is launched from the `streamlit/` directory.

Usage
-----
Import this module before any `src.*` import:

    import utils.path_setup  # noqa: F401
"""

import sys
from pathlib import Path

# ----------------------------------------------------------
# Resolve project root (two levels up from this file)
# streamlit/utils/path_setup.py  →  streamlit/  →  project root
# ----------------------------------------------------------

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])

if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
