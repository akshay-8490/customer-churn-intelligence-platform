"""
Project Settings Configuration
Project: Customer Churn Intelligence Platform
Description: Contains project-level constants, settings, and hyperparameters
             such as random state, test size, target column, etc.
"""

# ==========================================================
# General Settings
# ==========================================================

VERSION = "0.1.0"
LOG_LEVEL = "INFO"

# ==========================================================
# Machine Learning Configuration
# ==========================================================

RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COLUMN = "Churn"
MODEL_NAME = "logistic_regression"

# ==========================================================
# Exports
# ==========================================================

__all__ = [
    "VERSION",
    "LOG_LEVEL",
    "RANDOM_STATE",
    "TEST_SIZE",
    "TARGET_COLUMN",
    "MODEL_NAME",
]
