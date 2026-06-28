"""
Project Path Configuration
Project: Customer Churn Intelligence Platform
Description: Centralizes all project paths so that no notebook or module
             contains hardcoded directory names, and automatically creates
             necessary output directories.
"""

from pathlib import Path

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# ==========================================================
# Dataset Files
# ==========================================================

ML_DATASET_PATH = RAW_DATA_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
BUSINESS_DATASET_PATH = RAW_DATA_DIR / "Telco_customer_churn.xlsx"

# ==========================================================
# Application Directories
# ==========================================================

STREAMLIT_DIR = PROJECT_ROOT / "streamlit"
DASHBOARD_DIR = PROJECT_ROOT / "powerbi"

# ==========================================================
# Output Directories
# ==========================================================

MODELS_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DASHBOARD_DIR = REPORTS_DIR / "dashboard"
REPORTS_MODEL_DIR = REPORTS_DIR / "model"
REPORTS_EXPLAINABILITY_DIR = REPORTS_DIR / "explainability"
REPORTS_FIGURES_DIR = REPORTS_DIR / "figures"

# ==========================================================
# Processed Outputs
# ==========================================================

PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.pkl"
PROCESSED_DATASET_PATH = PROCESSED_DATA_DIR / "ml_dataset_processed.csv"

# ==========================================================
# Development Directories
# ==========================================================

DOCS_DIR = PROJECT_ROOT / "docs"
TESTS_DIR = PROJECT_ROOT / "tests"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# ==========================================================
# Automatic Directory Creation
# ==========================================================

DIRECTORIES = [
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    ARTIFACTS_DIR,
    REPORTS_DIR,
    REPORTS_DASHBOARD_DIR,
    REPORTS_MODEL_DIR,
    REPORTS_EXPLAINABILITY_DIR,
    REPORTS_FIGURES_DIR,
]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "INTERIM_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "ML_DATASET_PATH",
    "BUSINESS_DATASET_PATH",
    "PREPROCESSOR_PATH",
    "PROCESSED_DATASET_PATH",
    "STREAMLIT_DIR",
    "DASHBOARD_DIR",
    "MODELS_DIR",
    "ARTIFACTS_DIR",
    "REPORTS_DIR",
    "REPORTS_DASHBOARD_DIR",
    "REPORTS_MODEL_DIR",
    "REPORTS_EXPLAINABILITY_DIR",
    "REPORTS_FIGURES_DIR",
    "DOCS_DIR",
    "TESTS_DIR",
    "NOTEBOOKS_DIR",
]