# 📊 Customer Churn Intelligence Platform

An end-to-end Machine Learning, Explainable AI (XAI), and Business Intelligence (BI) platform built to predict customer churn, explain predictive decisions, evaluate revenue exposure, and automate customer retention campaigns. 

This platform features a dual-dashboard architecture: an interactive, publication-ready **Power BI Executive Dashboard** for advanced business reporting, and a custom **Streamlit Web Application** for real-time model inference and explainability.

---

## ⚡ Power BI Dashboard & Data Modeling

The flagship business dashboard is built in Power BI Desktop and located in the [powerbi/](file:///d:/customer-churn-intelligence-platform/powerbi) directory as **[Customer_Churn_Intelligence.pbix](file:///d:/customer-churn-intelligence-platform/powerbi/Customer_Churn_Intelligence.pbix)**.

### Data Flow & Automated Export
The backend Python machine learning pipeline dynamically constructs, enriches, and exports a unified analytical dataset to **`reports/dashboard/dashboard_dataset.csv`**. The Power BI report links directly to this file, ensuring that model retraining or prediction updates instantly propagate to the BI charts upon refresh.

### Analytical Schema & DAX Measures
The dataset consolidates customer identities, active service details, churn risk probabilities, K-Means customer personas, and prioritized retention recommendations. Within the Power BI data model, advanced analytical measures are implemented using **DAX** (Data Analysis Expressions):

- **Total MRR at Risk**: Sum of monthly charges weighted by predictive churn probability:
  $$\text{MRR at Risk} = \sum \left( \text{Monthly Charges} \times \text{Churn Probability} \right)$$
- **Expected Campaign ROI**: Protectable monthly revenue per dollar spent on retention campaigns:
  $$\text{Campaign ROI} = \frac{\text{Total MRR at Risk}}{\text{Total Estimated Campaign Cost}}$$
- **Churn Rate Metrics**: Side-by-side comparison of actual historical churn against the predictive expected churn rate.

### Dashboard Pages
1. **Executive Churn Overview**: High-level KPIs (Total MRR, Churn Rate, count of High/Critical Risk accounts) and interactive monthly revenue exposure charts.
2. **Customer Segmentation & Personas**: Detailed breakdowns of customer groups generated via machine learning clustering (e.g., *High-Value At-Risk*, *Loyal Long-Term*) sliced by contract types and payment methods.
3. **Retention Campaign ROI Tracker**: Financial planning view showing expected MRR saved vs. campaign costs for outbound discount upgrades, tech support trials, and loyalty credits.

---

## 🖥️ Streamlit Web Application

The **Streamlit Web Application** provides an interactive playground for real-time customer churn prediction and model explainability:

1. **📊 Executive Dashboard**  
   Quick overview of customer churn, revenue risk, and Plotly distributions matching the KPI definitions in Power BI.
2. **🎯 Predict Churn**  
   Interactive input form that feeds customer details directly into the inference pipeline, displaying predicted probability, risk badges, and recommended actions.
3. **🧠 Model Explainability**  
   Visualizes Permutation Feature Importance and SHAP (Beeswarm, Summary) plots to explain how model attributes drive predictions globally.
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
├── powerbi/                # Power BI Desktop Report Files
│   └── Customer_Churn_Intelligence.pbix  # Primary executive business report
├── reports/
│   ├── dashboard/          # Consolidated dataset exported for Power BI import
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

## 🏃 Running the Applications

### 1. Refreshing Power BI Dashboard Data
To update the underlying analytics in Power BI with new predictions or model runs:
- Step 1: Run the analytical pipelines via Jupyter notebooks (e.g. `notebooks/07_business_insights.ipynb`) to refresh the CSV export.
- Step 2: Open **`powerbi/Customer_Churn_Intelligence.pbix`** in Power BI Desktop.
- Step 3: Click **Refresh** in the home ribbon to reload the updated model metrics.

### 2. Launching the Streamlit Interface
To run the Streamlit web application:
```bash
streamlit run streamlit/app.py
```

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
