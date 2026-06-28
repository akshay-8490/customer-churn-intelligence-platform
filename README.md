# 📊 Customer Churn Intelligence Platform

An end-to-end Machine Learning, Explainable AI (XAI), and Business Intelligence platform built to predict customer churn, explain predictive decisions, evaluate revenue exposure, and automate customer retention campaigns.

This platform translates raw dataset records into clean dashboard indicators, categorizes portfolios via K-Means clustering, and assigns optimized business actions to secure recurring revenue.

---

## 🚀 Key Modules & Streamlit App

The front-end Web Application integrates the entire pipeline into an interactive decision-support tool. It includes:

1. **📊 Executive Dashboard**  
   Real-time business indicators (MRR, Churn Rate, Revenue at Risk, high-risk customer counts) and interactive filters (Risk Segment, Contract, Internet Service) with Plotly distributions.
2. **🎯 Predict Churn**  
   Interactive input form that feeds customer details directly into the inference pipeline, displaying predicted probability, risk badges, and recommended actions.
3. **🧠 Model Explainability**  
   Visualizes Permutation Feature Importance and SHAP (Beeswarm, Summary) plots to display how demographic, service, and billing attributes drive churn.
4. **👥 Customer Insights**  
   Portfolio analysis detailing customer demographics, service adoption rates, billing patterns, and tenure distributions.
5. **💼 Business Recommendations**  
   Actionable ROI projections, campaign cost estimations, and priority lists for targeted customer retention campaigns.
6. **ℹ️ About Project**  
   Detailed documentation of the technology stack, project highlights, future enhancements, and pipeline architecture.

---

## 📁 Project Architecture

The codebase follows a modular design pattern separating preprocessing, pipeline execution, business reasoning, and representation:

```
├── artifacts/              # Serialized ML models, preprocessors, and metadata
├── data/
│   ├── raw/                # Source CSV and Excel files (IBM Telco Dataset)
│   ├── interim/            # Intermediate CSV formats
│   └── processed/          # Preprocessed data matrices ready for training
├── models/                 # Alternate model binary pickles (RF, XGBoost, etc.)
├── notebooks/              # Step-by-step Jupyter EDA and Model pipelines
├── reports/
│   ├── dashboard/          # Exported business CSV indicators
│   ├── explainability/     # Feature importance rankings
│   └── figures/            # Static charts and SHAP summary plots
├── src/                    # Core Python Source Package
│   ├── business/           # Business logic modules (revenue, clustering, actions)
│   │   ├── artifact_loader.py
│   │   ├── churn_driver_analysis.py
│   │   ├── customer_personas.py
│   │   ├── customer_portfolio.py
│   │   ├── dashboard_export.py
│   │   ├── retention_engine.py
│   │   └── revenue_analysis.py
│   ├── config/             # Path and environment setting constants
│   ├── data/               # Loading, auditing, and comparing data structures
│   ├── explainability/     # SHAP tree/linear models and local explanations
│   ├── features/           # Feature creators and column transformers
│   ├── utils/              # Print and directory creation helper utilities
│   └── visualization/      # Matplotlib/Seaborn visualization helpers
└── streamlit/              # Streamlit Web App components and page scripts
```

---

## ⚙️ Setup & Installation

### Prerequisite: Python 3.10+

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd customer-churn-intelligence-platform
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   
   # Linux / macOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Running the Application

To run the Streamlit web application:

```bash
streamlit run streamlit/app.py
```

Open `http://localhost:8501` in your browser to view the interactive platform.

---

## 🤖 Machine Learning & Feature Engineering Pipeline

### Derived Features (`src/features/feature_creator.py`)
- **TenureGroup**: Bins tenure into business milestones (New, Emerging, Established, Loyal, Long-Term).
- **MonthlyChargeGroup**: Splices monthly spending into quartile tiers (Low, Medium, High, Premium).
- **TotalServices**: Sums active service additions (Phone, Online Security, Tech Support, Streaming, etc.).
- **AvgMonthlySpend**: Calculated as `TotalCharges / tenure` to evaluate average customer value.
- **SecurityRisk**: Flag for customers subscribing to neither Online Security nor Tech Support.
- **StreamingUser**: Flag for active video streaming additions.

### Machine Learning Engine (`src/features/preprocessor_builder.py`)
- **Pipeline**: Fits a `ColumnTransformer` wrapping a `StandardScaler` for numeric values and `OneHotEncoder` for category variables.
- **Auto ID Removal**: Autodetects and drops unique unique identifiers (`customerID`/`CustomerID`) to prevent dimensional blow-up.
- **Model**: A tuned **Logistic Regression** classifier (trained using balanced class weights, `L1` penalty, and a custom `0.55` decision threshold) yielding a cross-validated **ROC-AUC of 0.839**.

---

## 💼 Business Logic & Campaign ROI Engine

### Customer Personas (`src/business/customer_personas.py`)
Applies a `KMeans(n_clusters=4)` clustering model on scaled customer value attributes to segment customers into:
- **Loyal Long-Term Customers** (High tenure, high spending, low churn risk)
- **High-Value At-Risk Customers** (High monthly spending, elevated churn risk)
- **New Price-Sensitive Customers** (Short tenure, basic service configuration)
- **Stable Family Customers** (Multi-service accounts with low attrition rates)

### Retention Action & Priority Engine (`src/business/retention_engine.py`)
- **Priority Score**: Calculated as `MonthlyCharges * Churn_Probability` representing the expected monthly recurring revenue (MRR) at risk for each account.
- **Retention Campaigns**:
  - `Churn_Probability > 0.7`: Escalates to Outbound Upgrade/Discount Offer or Executive Calls (Estimated Cost: `$15.00`).
  - `Churn_Probability > 0.4`: Escalates to Support Outreach/Free Support Trials or Plan Reviews (Estimated Cost: `$5.00` / `$0.00`).
  - `Others`: Fallback to Loyalty summary thank-you emails (Estimated Cost: `$0.00`).

---

## 🛠️ Development & Quality Assurance

All modified source files are compiled to prevent runtime errors:
```powershell
Get-ChildItem -Path src -Filter *.py -Recurse | ForEach-Object { python -m py_compile $_.FullName }
```

### Key Safety Highlights
- **Dynamic Preprocessor Lookups**: Prevents crashes if feature order changes during future model training.
- **Pipeline Unwrapping**: Dynamically extracts core estimators when wrapped inside scikit-learn `Pipeline` objects.
- **Segment DataFrame Integrity**: Features defensive segment lookup queries protecting the dashboard from `KeyError` crashes.
- **Safe Inference Bounds**: Features conditional fallbacks in dynamic quantile grouping (`pd.qcut`) to support single-row predictions without throwing unique-bin errors.
