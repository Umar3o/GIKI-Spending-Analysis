# GIKI Student Spending Analysis

A data-driven study of monthly variable spending patterns among GIKI hostel students — using primary survey data, regression modelling, and a rule-based financial health classifier to answer the question: are students' allowances actually enough?

---

## Research Question

Do demographic features (age, year of study, faculty group, gender) predict monthly variable spending among GIKI hostel students, and are students' monthly allowances sufficient to cover their actual expenditure?

This study tests whether the assumption established by Deaton and Muellbauer (1980) — that demographic variables predict household spending — holds in a Pakistani residential university context.

---

## Repository Structure

```
GIKI-Spending-Analysis/
├── data/
│   ├── raw/                    ← original survey responses (Excel)
│   └── processed/              ← cleaned dataset (CSV)
├── notebooks/
│   ├── 01_preprocessing.ipynb  ← data cleaning and feature engineering
│   ├── 02_eda.ipynb            ← exploratory data analysis and charts
│   └── 03_modelling.ipynb      ← model training, comparison, and evaluation
├── outputs/                    ← saved model, charts, comparison tables
│   ├── best_model.joblib
│   ├── model_comparison.csv
│   ├── feature_importance.csv
│   └── *.png
└── app/
    ├── app.py                  ← Flask backend
    ├── templates/
    │   └── index.html          ← single-page frontend
    └── static/
        └── style.css
```

---

## How to Run

**1. Install dependencies**

```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib flask openpyxl
```

**2. Place the raw data file in `data/raw/`**

The file should be named `raw_data.csv`.

**3. Run the notebooks in order**

Open each notebook in VS Code and run all cells:

```
01_preprocessing.ipynb  →  02_eda.ipynb  →  03_modelling.ipynb
```

**4. Launch the demo app**

```bash
cd app
flask run
```

Then open `http://127.0.0.1:5000` in your browser.

---

## Key Findings

- **47.9%** of surveyed students are spending beyond their monthly allowance
- The median student has a monthly deficit of **PKR 1,000** — allowances are not keeping up with actual spend
- **Senior students** spend PKR 6,130 less per month than Freshmen on average, indicating that financial management improves over the degree lifecycle
- **Engineering students** are the highest-spending faculty group; FCSE students spend approximately PKR 7,374 less per month
- A cross-validated MAE of **PKR 15,194** indicates that demographic features alone have limited predictive power — individual habits, not demographics, are the dominant driver of spending at GIKI

---

## Models Compared

Five regression models were trained and evaluated using 5-fold cross-validation. Mean Absolute Error (MAE) in PKR is reported as mean ± standard deviation across folds.

| Model | Mean MAE (PKR) | Std MAE (PKR) |
|---|---|---|
| Linear Regression | 15,234 | 1,714 |
| **Ridge** | **15,194** | **1,708** |
| Lasso | 15,233 | 1,714 |
| Random Forest | 15,212 | 1,544 |
| KNN | 16,238 | 1,895 |

**Ridge Regression** was selected as the final model. It achieved the lowest cross-validated MAE and produces interpretable coefficients that directly answer the research question. The regularisation penalty handles mild multicollinearity in a small dataset more robustly than unpenalised linear regression.

---

## Financial Health Classifier

The classifier compares the model's predicted spend against a student's reported monthly allowance and returns one of three labels:

| Status | Condition |
|---|---|
| Saving | Allowance > Predicted Spend + 5% buffer |
| Balanced | Within ±5% of predicted spend |
| Overspending Risk | Allowance < Predicted Spend |

---

## Literature

| Reference | Relevance |
|---|---|
| Sabri & MacDonald (2010), *Cross-Cultural Communication* | Primary methodological reference — survey + regression on residential university students |
| Lusardi, Mitchell & Curto (2010), *Journal of Consumer Affairs* | Establishes low financial literacy as a driver of student overspending |
| Deaton & Muellbauer (1980), *American Economic Review* | Validates use of demographic features as expenditure predictors in Western markets |
| Dillman, Smyth & Christian (2014), *Internet, Phone, Mail & Mixed-Mode Surveys* | Validates short survey design for reliable self-reported spending data |

---

## Team

| Name | Student ID |
|---|---|
| Umar Abdullah | 2024644 |
| Rohaan Jamshaid | 2024442 |

**GIK Institute of Engineering Sciences and Technology**
DS211 — Theory of Data Science
Term Project, Spring 2026
