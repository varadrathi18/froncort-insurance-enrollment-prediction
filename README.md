# Insurance Enrollment Prediction + Outreach Assistant

## Project Overview

This project was developed as part of the **Froncort.AI Machine Learning Intern Assignment**.

The objective is to build an end-to-end machine learning system that predicts whether an employee will enroll in a voluntary insurance plan and expose the trained model through a tool-based Outreach Assistant that helps HR teams prioritize employee outreach while respecting fairness and leakage constraints.

The project covers the complete machine learning workflow, including data investigation, cleaning, feature engineering, model development, evaluation, and deployment of prediction tools.

---

# Project Structure

```
project/
│
├── data/
│   ├── employees_raw.csv
│   ├── region_benefit_profiles.csv
│   ├── employees_final.csv
│   └── predictions.csv
│
├── models/
│   └── final_model.pkl
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_model_development.ipynb
│   └── 05_final_submission.ipynb
│
├── report.md
├── AI_USAGE.md
├── requirements.txt
└── README.md
```

---

# Project Workflow

The project follows the complete machine learning pipeline:

1. Data Investigation
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Model Training
6. Model Evaluation
7. Outreach Assistant Development
8. Prediction Generation

---

# Machine Learning Model

The final production model is a **Random Forest Classifier**.

Evaluation includes:

- Stratified Train/Test Split
- 5-Fold Cross Validation
- ROC-AUC
- Precision, Recall and F1-Score
- Confusion Matrix
- Majority Class Baseline
- Rule-Based Baseline
- Precision@K for outreach prioritization

The final model intentionally excludes the identified leakage feature (`legacy_propensity_score`).

---

# Outreach Assistant

The Outreach Assistant provides four tools:

### 1. Predict Enrollment

Predicts whether a selected employee is likely to enroll and returns:

- Prediction
- Probability
- Confidence level

---

### 2. Rank Outreach Candidates

Ranks employees within a selected region based on predicted enrollment probability and returns the top employees according to the region's available HR outreach capacity.

---

### 3. Lookup Region Profile

Displays operational statistics for a selected region, including:

- Historical enrollment rate
- Average salary
- Average premium cost
- Broker rating
- Outreach capacity
- Enrollment window

---

### 4. Explain Prediction

Generates a natural-language explanation describing the primary factors influencing an employee's prediction.

The explanation intentionally excludes:

- Age
- Gender
- Marital Status
- `legacy_propensity_score`

to satisfy fairness and leakage requirements.

---

# Safety Features

The project includes several responsible AI safeguards:

- Refuses to use `legacy_propensity_score` for prediction or explanation.
- Prevents explanations from referencing protected demographic attributes.
- Separates operational features from identified leakage features.
- Uses the non-leaky Random Forest model as the final deployment model.

---

# Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Project

Execute the notebooks in the following order:

1. `01_data_understanding.ipynb`
2. `02_data_cleaning.ipynb`
3. `03_EDA.ipynb`
4. `04_model_development.ipynb`
5. `05_final_submission.ipynb`

---

# Repository Contents

- Cleaned dataset
- Trained Random Forest model
- Prediction outputs
- Outreach Assistant tools
- Project report
- AI usage declaration
- Requirements file

---

# Author - Varad Rathi