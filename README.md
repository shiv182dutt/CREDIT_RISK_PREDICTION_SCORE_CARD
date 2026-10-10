# Credit Risk Probability of Default (PD) Scorecard


                    ┌──────────────────────┐
                    │   BUSINESS PROBLEM   │
                    │ Predict Loan Default  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │       DATA           │
                    │ 100,000 Applicants   │
                    │ 24 Variables        │
                    │ Bad Rate = 6.82%     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   DATA CLEANING      │
                    │ Missing Values       │
                    │ Sentinel Values      │
                    │ Outliers             │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │        EDA           │
                    │ Distribution         │
                    │ Correlation          │
                    │ Bad Rate Analysis    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   TRAIN / TEST       │
                    │ 70% Train            │
                    │ 30% Test             │
                    │ Stratified Split     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │       BINNING        │
                    │ Numerical Variables  │
                    │ Risk Groups           │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │      WOE / IV        │
                    │ Risk Transformation  │
                    │ Feature Strength     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ FEATURE SELECTION    │
                    │ IV + Correlation     │
                    │ Business Logic       │
                    └──────────┬───────────┘
                               ↓
             ┌─────────────────┴─────────────────┐
             ↓                                   ↓
   ┌──────────────────────┐           ┌──────────────────────┐
   │  CHAMPION MODEL      │           │ CHALLENGER MODELS    │
   │ WOE + Logistic       │           │ Random Forest        │
   │ Regression           │           │ XGBoost              │
   └──────────┬───────────┘           └──────────┬───────────┘
              │                                  │
              ↓                                  ↓
   ┌──────────────────────┐           ┌──────────────────────┐
   │ Probability of       │           │ Model Comparison     │
   │ Default (PD)         │           │ AUC / Gini / KS      │
   └──────────┬───────────┘           │ Brier / AUC Gap      │
              │                       └──────────┬───────────┘
              ↓                                  ↓
   ┌──────────────────────┐           ┌──────────────────────┐
   │ SCORECARD            │           │ SHAP                 │
   │ PD → Credit Score    │           │ XGBoost Explainability│
   │ Score → Risk Band    │           └──────────┬───────────┘
   └──────────┬───────────┘                      │
              └────────────────┬─────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │       VALIDATION     │
                    │ AUC = 0.5969         │
                    │ Gini = 0.1938        │
                    │ KS = 0.1455          │
                    │ Brier = 0.0630       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │     MONITORING       │
                    │ PSI = ~0.0007        │
                    │ CSI                  │
                    │ Bad Rate Stability  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │     DEPLOYMENT       │
                    │       FastAPI        │
                    │      /predict        │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │      STREAMLIT       │
                    │ Interactive Dashboard│
                    └──────────┬───────────┘
                               ↓
              ┌────────────────────────────────┐
              │ FINAL BUSINESS OUTPUT          │
              │                                │
              │ Probability of Default (PD)   │
              │ Credit Score                   │
              │ Risk Band                      │
              └────────────────────────────────┘

## 1. PROJECT OVERVIEW

This project builds an end-to-end **Credit Risk Probability of Default (PD) Scorecard** for a lending/loan-origination use case.

**Objective:** estimate an applicant's Probability of Default (PD), convert it into an interpretable credit score, assign a risk band, validate the model, monitor stability, compare ML challengers, and deploy the model through an API and dashboard.

### End-to-End Flow

**Raw Applicant Data → Data Cleaning → EDA → Train/Test Split → Binning → WOE/IV → Logistic Regression Scorecard → Validation → Challenger Models → SHAP → Monitoring → FastAPI → Streamlit**

---

## 2. BUSINESS PROBLEM

Financial institutions need to estimate the likelihood that a borrower will default before approving or pricing a loan.

This project answers:

> **Given an applicant's financial and credit characteristics, what is the estimated Probability of Default, what credit score should be assigned, and what risk band does the applicant belong to?**

Business uses include:
- Loan origination
- Credit risk assessment
- Applicant risk ranking
- Risk-based decision support
- Portfolio/model monitoring
- Model validation

The scorecard is a **decision-support model** and does not replace complete credit policy, affordability checks, fraud controls, underwriting rules, regulatory requirements, or human review.

---

## 3. CREDIT RISK DOMAIN

### Probability of Default (PD)

**Bad = 1 → Bad / Default borrower**  
**Bad = 0 → Good borrower**

Therefore:

**Higher PD = Higher estimated credit risk**  
**Lower PD = Lower estimated credit risk**

The scorecard is designed so:

**Higher Credit Score = Lower Risk**  
**Lower Credit Score = Higher Risk**

---

## 4. DATASET

Synthetic credit-risk dataset designed to resemble an applicant-level lending dataset.

- **Rows:** 100,000 applicants
- **Columns:** 24
- **Bad Rate:** approximately **6.82%**
- **Target:** `Bad`
- **Sheets:** `Credit_Data`, `Data_Dictionary`, `Summary`

### Main Variables

**Applicant/Demographic:** `Customer_ID`, `Age`, `Number_of_Dependents`, `State`

**Income/Employment:** `Monthly_Income`, `Employment_Length_Years`, `Employment_Type`, `Years_at_Address`, `Home_Ownership`

**Credit Behaviour:** `Credit_Utilization`, `Number_of_Credit_Lines`, `Number_of_Open_Loans`, `Credit_History_Years`, `Recent_Inquiries_6M`, `Number_of_Delinquencies_30`, `Number_of_Delinquencies_60`, `Number_of_Delinquencies_90`

**Debt/Loan:** `Total_Debt`, `Debt_to_Income`, `Loan_Amount`, `Loan_Tenure_Months`, `Interest_Rate`, `Loan_Purpose`

**Target:** `Bad`

---

## 5. DATA CLEANING

Cleaning included:

- Converted 30-day delinquency sentinel values `96` and `98` to missing.
- Removed ages outside 18–100.
- Created `Income_Missing`, `DTI_Missing`, and `Employment_Length_Missing`.
- Median-imputed selected numerical missing values.
- Applied 1st/99th percentile capping to selected numerical variables.

**Production consideration:** in a production pipeline, imputation and capping thresholds should be learned from training data only and then applied unchanged to validation/test/production data.

---

## 6. EDA AND FEATURE RELATIONSHIPS

Important correlations:

- `Credit_History_Years` vs `Age` = **0.9681**
- `Credit_Utilization` vs `Interest_Rate` = **0.8059**
- `Credit_Utilization` vs `Debt_to_Income` = **0.4424**

These relationships were considered during feature selection to reduce redundancy.

---

## 7. TRAIN/TEST SPLIT

A stratified split was used:

- **70% Training**
- **30% Test**
- `random_state = 42`
- `stratify = y`

The same holdout test population was used for challenger comparison.

---

## 8. BINNING

Continuous variables were converted into risk groups using quantile-based binning (`qcut`) with separate handling for missing values and discrete variables.

Reusable implementation:

`src/binning.py`

---

## 9. WOE AND IV

Project convention:

**WOE = ln(%Good / %Bad)**

- Positive WOE → relatively more good borrowers
- Negative WOE → relatively more bad borrowers

WOE/IV logic is implemented in:

`src/woe_iv.py`

### Selected IV Results

| Feature | IV |
|---|---:|
| Credit_History_Years | 0.043025 |
| Age | 0.042711 |
| Credit_Utilization | 0.032756 |
| Interest_Rate | 0.027769 |
| Debt_to_Income | 0.026131 |
| Employment_Length_Years | 0.017351 |
| Monthly_Income | 0.014822 |
| Recent_Inquiries_6M | 0.009027 |
| Number_of_Open_Loans | 0.008472 |
| Loan_Amount | 0.003726 |

---

## 10. FINAL CHAMPION FEATURES

The champion scorecard uses eight variables:

```text
Credit_History_Years
Credit_Utilization
Debt_to_Income
Employment_Length_Years
Monthly_Income
Number_of_Delinquencies_30
Number_of_Delinquencies_60
Number_of_Delinquencies_90
```

`Age` was excluded because of its very high correlation with `Credit_History_Years`.

`Interest_Rate` was excluded because of its high correlation with `Credit_Utilization` and lower IV than the selected variable.

---

## 11. CHAMPION MODEL — WOE + LOGISTIC REGRESSION

The production champion is:

**WOE-transformed variables + Logistic Regression**

The model estimates:

**PD = P(Bad = 1 | Applicant Characteristics)**

### Champion Coefficients

| Feature | Coefficient |
|---|---:|
| Credit_History_Years_WOE | -0.951241 |
| Credit_Utilization_WOE | -0.797219 |
| Debt_to_Income_WOE | -0.681773 |
| Employment_Length_Years_WOE | -0.919838 |
| Monthly_Income_WOE | -0.256850 |
| Number_of_Delinquencies_30_WOE | -0.860103 |
| Number_of_Delinquencies_60_WOE | -0.833179 |
| Number_of_Delinquencies_90_WOE | -0.921746 |

The negative coefficients are consistent with the selected WOE convention.

---

## 12. CHAMPION PERFORMANCE

| Metric | Result |
|---|---:|
| Train AUC | **0.5987** |
| Test AUC | **0.5969** |
| Gini | **0.1938** |
| KS | **0.1455** |
| Brier Score | **0.0630** |
| Train/Test AUC Gap | **0.0018** |

### Interpretation

The model has a very small train/test AUC gap, indicating stable generalization on this holdout sample.

The **0.5969 test AUC** also shows that the synthetic dataset has relatively weak standalone discriminatory signal. This result is reported transparently rather than hidden.

---

## 13. SCORECARD METHODOLOGY

Parameters:

- **Base Score:** 600
- **Base Odds:** 50
- **PDO:** 20

```text
Factor = PDO / ln(2)
       = 28.853901

Offset = Base Score - Factor × ln(Base Odds)
       = 487.122876
```

The score is linked to the model logit so:

**Higher score = Lower estimated risk**

---

## 14. RISK BANDS

| Score | Risk Band |
|---:|---|
| >= 575 | Low Risk |
| 565–574.99 | Medium Risk |
| 550–564.99 | High Risk |
| < 550 | Very High Risk |

### Test Risk Distribution

| Risk Band | Applicants |
|---|---:|
| High Risk | 12,629 |
| Medium Risk | 10,627 |
| Low Risk | 4,183 |
| Very High Risk | 2,561 |

### Observed Bad Rates

| Risk Band | Bad Rate |
|---|---:|
| Low Risk | **4.16%** |
| Medium Risk | **5.39%** |
| High Risk | **7.79%** |
| Very High Risk | **12.34%** |

The increasing bad rate across risk bands demonstrates useful risk ranking.

---

## 15. VALIDATION

Validation metrics:

- **AUC:** 0.5969
- **Gini:** 0.1938
- **KS:** 0.1455
- **Brier Score:** 0.0630

### PD Calibration

| Risk Band | Avg PD | Actual Bad Rate |
|---|---:|---:|
| Low Risk | 3.91% | 4.36% |
| Medium Risk | 5.68% | 5.70% |
| High Risk | 8.39% | 8.16% |
| Very High Risk | 13.96% | 13.99% |

---

## 16. CHALLENGER MODELS

Two nonlinear models were tested:

1. **Random Forest**
2. **XGBoost**

Purpose: determine whether nonlinear models provide additional predictive value over the traditional scorecard.

---

## 17. RANDOM FOREST

Random Forest used cleaned/raw features with numerical imputation and one-hot encoding for categorical variables.

| Metric | Random Forest |
|---|---:|
| Train AUC | **0.6854** |
| Test AUC | **0.5951** |
| Gini | **0.1901** |
| KS | **0.1375** |
| Brier Score | **0.2355** |

### Overfitting

```text
Train AUC = 0.6854
Test AUC  = 0.5951
Gap       = 0.0904
```

Random Forest did not outperform the champion and was rejected.

### Top Feature Importance

| Feature | Importance |
|---|---:|
| Credit_History_Years | 0.1216 |
| Credit_Utilization | 0.1181 |
| Age | 0.1157 |
| Debt_to_Income | 0.0975 |
| Interest_Rate | 0.0819 |
| Employment_Length_Years | 0.0794 |
| Monthly_Income | 0.0558 |
| Total_Debt | 0.0469 |
| Loan_Amount | 0.0423 |
| Years_at_Address | 0.0335 |

---

## 18. XGBOOST

XGBoost was evaluated as a gradient-boosting challenger.

| Metric | XGBoost |
|---|---:|
| Train AUC | **0.7283** |
| Test AUC | **0.5860** |
| Gini | **0.1719** |
| KS | **0.1280** |
| Brier Score | **0.0633** |

### Overfitting

```text
Train AUC = 0.7283
Test AUC  = 0.5860
Gap       = 0.1423
```

XGBoost showed substantial overfitting and did not outperform the champion.

---

## 19. SHAP EXPLAINABILITY

SHAP was used to explain the XGBoost challenger.

### Top SHAP Drivers

| Rank | Feature | Mean Absolute SHAP |
|---:|---|---:|
| 1 | Credit_History_Years | 0.1245 |
| 2 | Employment_Length_Years | 0.1069 |
| 3 | Credit_Utilization | 0.1058 |
| 4 | Recent_Inquiries_6M | 0.0638 |
| 5 | Age | 0.0591 |
| 6 | Total_Debt | 0.0578 |
| 7 | Debt_to_Income | 0.0537 |
| 8 | Monthly_Income | 0.0506 |
| 9 | Interest_Rate | 0.0383 |
| 10 | Years_at_Address | 0.0366 |

SHAP was used for model explanation, not causal inference.

Saved artifacts:

```text
outputs/metrics/xgboost_shap_importance.csv
outputs/figures/xgboost_shap_summary.png
outputs/figures/xgboost_shap_importance_bar.png
```

---

## 20. FINAL THREE-MODEL COMPARISON

| Metric | WOE Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Test AUC | **0.5969** | 0.5951 | 0.5860 |
| Gini | **0.1938** | 0.1901 | 0.1719 |
| KS | **0.1455** | 0.1375 | 0.1280 |
| Brier Score | **0.0630** | 0.2355 | 0.0633 |
| Train AUC | 0.5987 | 0.6854 | 0.7283 |
| AUC Gap | **0.0018** | 0.0904 | 0.1423 |

### Final Decision

**CHAMPION:** WOE + Logistic Regression Scorecard

**CHALLENGERS:** Random Forest, XGBoost

The Logistic Regression scorecard was retained because it had the best holdout AUC, Gini and KS, the smallest train/test AUC gap, and strong interpretability and scorecard transparency.

---

## 21. MONITORING

Monitoring included:

- Population Stability Index (PSI)
- Characteristic Stability Index (CSI)
- Train/test bad-rate comparison

### PSI

Champion PD PSI:

**approximately 0.0007**

### Bad Rate Stability

- Train bad rate: **approximately 6.82%**
- Test bad rate: **approximately 6.82%**
- Difference: **0.00 percentage points**

### CSI

| Variable | CSI |
|---|---:|
| Credit_History_Years_WOE | 0.0004 |
| Credit_Utilization_WOE | 0.0003 |
| Debt_to_Income_WOE | 0.0003 |
| Employment_Length_Years_WOE | 0.0002 |
| Monthly_Income_WOE | 0.0001 |
| Number_of_Delinquencies_30_WOE | 0.0000 |
| Number_of_Delinquencies_60_WOE | 0.0000 |
| Number_of_Delinquencies_90_WOE | 0.0000 |

No meaningful train/test population or variable shift was observed in this development dataset.

---

## 22. DEPLOYMENT

The champion model was deployed using **FastAPI**.

### Endpoint

```text
POST /predict
```

### Example response

```json
{
    "PD": 0.097045,
    "Score": 551.48,
    "Risk_Band": "High Risk"
}
```

The service returns:

- Probability of Default
- Credit Score
- Risk Band

---

## 23. STREAMLIT DASHBOARD

A Streamlit dashboard was created for interactive applicant scoring.

Inputs include:

- Credit history
- Credit utilization
- DTI
- Employment length
- Monthly income
- 30-day delinquency
- 60-day delinquency
- 90-day delinquency

Outputs:

- PD
- Credit Score
- Risk Band

### Architecture

```text
User
  ↓
Streamlit Dashboard
  ↓
FastAPI /predict
  ↓
Prediction Logic
  ↓
WOE Transformers
  ↓
Logistic Regression
  ↓
PD + Credit Score + Risk Band
```

---

## 24. PROJECT ARCHITECTURE

```text
credit-risk-pd/
│
├── data/
│   ├── raw/
│   │   └── credit_risk_synthetic_100k_fixed.xlsx
│   └── processed/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_woe_iv.ipynb
│   ├── 03_scorecard.ipynb
│   ├── 04_validation.ipynb
│   ├── 05_challenger.ipynb
│   └── 06_monitoring.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── binning.py
│   ├── woe_iv.py
│   ├── scorecard.py
│   ├── model.py
│   ├── validation.py
│   ├── monitoring.py
│   ├── utils.py
│   └── predict.py
│
├── outputs/
│   ├── figures/
│   ├── metrics/
│   ├── scorecard/
│   └── models/
│
├── app/
│   ├── api.py
│   └── dashboard.py
│
├── tests/
├── requirements.txt
├── README.md
├── .gitignore
└── main.py
```

---

## 25. IMPORTANT OUTPUTS

```text
outputs/models/champion_logistic_model.pkl
outputs/models/woe_transformers.pkl
outputs/scorecard/final_scorecard.csv

outputs/metrics/final_validation_metrics.csv
outputs/metrics/final_3_model_comparison.csv
outputs/metrics/model_overfitting_comparison.csv
outputs/metrics/final_model_decision.csv

outputs/metrics/xgboost_shap_importance.csv
outputs/figures/xgboost_shap_summary.png
outputs/figures/xgboost_shap_importance_bar.png

outputs/metrics/monitoring_summary.csv
outputs/metrics/csi_results.csv
```

---

## 26. HOW TO RUN

### Create virtual environment

```bash
python -m venv .venv
```

### Activate on Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run notebooks

```text
01_eda.ipynb
02_woe_iv.ipynb
03_scorecard.ipynb
04_validation.ipynb
05_challenger.ipynb
06_monitoring.ipynb
```

### Run FastAPI

```bash
python -m uvicorn app.api:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Run Streamlit

```bash
python -m streamlit run app/dashboard.py
```

---

## 27. 30-SECOND INTERVIEW EXPLANATION

> "I developed an end-to-end credit-risk Probability of Default scorecard using a synthetic 100,000-applicant dataset with a 6.82% bad rate. I performed data cleaning, EDA, binning, WOE and IV analysis, selected eight key credit-risk variables, and developed a WOE Logistic Regression scorecard as the champion. The model achieved a test AUC of 0.5969, Gini of 0.1938 and KS of 0.1455. I then tested Random Forest and XGBoost as nonlinear challengers, but neither outperformed the champion and both showed larger train-test gaps. I used SHAP to explain the XGBoost challenger, implemented PSI/CSI monitoring, and deployed the champion through FastAPI and a Streamlit dashboard that returns PD, credit score and risk band."

---

## 28. KEY INTERVIEW ANSWERS

### Why WOE?

> "WOE converts variable values into a risk-oriented representation based on the distribution of good and bad accounts. It makes variables suitable for a traditional scorecard and improves interpretability."

### Why Logistic Regression?

> "Logistic Regression is well suited to binary default prediction and is highly interpretable. Combined with WOE, the coefficients can be translated into scorecard points."

### Why Random Forest?

> "I used Random Forest as a nonlinear challenger to test whether interactions and nonlinear relationships could improve predictive performance."

**Result: Test AUC = 0.5951**

It did not outperform the champion.

### Why XGBoost?

> "I used XGBoost as a gradient-boosting challenger to test whether a stronger nonlinear model could improve discrimination."

**Result: Test AUC = 0.5860**

It performed worse than the champion and had a train/test AUC gap of **0.1423**.

### Why SHAP?

> "I used SHAP to explain the XGBoost challenger and understand which variables were driving its predictions. The major drivers included credit history, employment length, credit utilization, recent inquiries, age, total debt and DTI."

### How did you select the champion?

> "I compared all models on the same holdout set using AUC, Gini, KS and Brier Score, and also considered the train/test performance gap and interpretability. WOE Logistic Regression achieved the best holdout discrimination and the smallest train/test gap, so I retained it as the champion."

### What does AUC 0.5969 mean?

> "The model's standalone discriminatory power on this synthetic dataset is relatively weak. I report that transparently. The project demonstrates the complete credit-risk modelling lifecycle rather than hiding a weak synthetic signal. With real data, I would investigate additional predictive variables, target definition, sample construction and out-of-time performance before production approval."

### How did you check stability?

> "I compared train and test performance and calculated PSI and CSI. The champion had a train/test AUC gap of approximately 0.0018, PD PSI of approximately 0.0007, and very low CSI values."

### What does the API return?

```text
PD
Credit Score
Risk Band
```

Example:

```json
{
    "PD": 0.097045,
    "Score": 551.48,
    "Risk_Band": "High Risk"
}
```

---

## 29. PROJECT STRENGTHS

- End-to-end credit-risk workflow
- 100K applicant dataset
- Business/domain understanding
- Data cleaning and EDA
- Binning
- WOE/IV
- Logistic Regression scorecard
- Credit score generation
- Risk segmentation
- Model validation
- PD calibration analysis
- Random Forest challenger
- XGBoost challenger
- SHAP explainability
- PSI monitoring
- CSI monitoring
- FastAPI deployment
- Streamlit dashboard
- Reusable Python modules
- Production-oriented architecture

---

## 30. PROJECT LIMITATIONS

This is a synthetic dataset and does not represent a real bank portfolio.

The test AUC of **0.5969** indicates relatively weak predictive signal.

The project does not claim regulatory approval or real-bank production approval.

A real production implementation would require additional work including:

- Real historical loan-performance data
- Clearly defined observation and performance windows
- Out-of-time validation
- Reject inference considerations
- Data lineage
- Model governance
- Fair-lending/bias assessment
- Regulatory documentation
- Independent model validation
- Production monitoring thresholds
- Recalibration/redevelopment policy

---

# 31. FINAL PROJECT SUMMARY

This project demonstrates the complete credit-risk PD modelling lifecycle:

**Business Problem**
→ **Data**
→ **Cleaning**
→ **EDA**
→ **Binning**
→ **WOE/IV**
→ **Feature Selection**
→ **Logistic Regression**
→ **Scorecard**
→ **PD**
→ **Credit Score**
→ **Risk Band**
→ **Validation**
→ **Random Forest**
→ **XGBoost**
→ **SHAP**
→ **PSI/CSI Monitoring**
→ **FastAPI**
→ **Streamlit**

### Final Champion

**WOE + Logistic Regression Scorecard**

### Final Test Performance

**AUC = 0.5969**  
**Gini = 0.1938**  
**KS = 0.1455**  
**Brier Score = 0.0630**

### Final Business Output

**Probability of Default + Credit Score + Risk Band**

The project demonstrates the broader credit-risk lifecycle of:

**Development → Validation → Challenger Testing → Explainability → Monitoring → Deployment**
