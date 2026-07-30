# Insurance Enrollment Prediction + Outreach Assistant

## Project Overview

This project predicts whether an employee will enroll in a voluntary insurance plan using machine learning and provides an Outreach Assistant that helps HR teams prioritize employee outreach based on limited regional outreach capacity.

The project was developed as part of the Froncort.AI ML Intern Assignment.

---

## Project Structure

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
│   ├── 03_model_development.ipynb
│   └── 04_final_submission.ipynb
│
├── report.md
├── AI_USAGE.md
├── requirements.txt
└── README.md
```

---

## Workflow

1. Data Investigation
2. Data Cleaning
3. Feature Engineering
4. Model Training
5. Model Evaluation
6. Outreach Assistant
7. Predictions Generation

---

## Selected Model

- Random Forest Classifier
- Legacy leakage feature excluded
- 5-Fold Cross Validation performed

---

## Agent Capabilities

The Outreach Assistant supports:

- Predict employee enrollment
- Rank outreach candidates by region
- Lookup region statistics
- Explain predictions safely
- Refuse to use leaky features

---

## Safety Features

The assistant:

- Refuses to use `legacy_propensity_score`.
- Does not explain predictions using age, gender, or marital status.

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run

Open the notebooks in order:

1. `01_data_understanding.ipynb`
2. `02_data_cleaning.ipynb`
3. `03_model_development.ipynb`
4. `04_final_submission.ipynb`

---

## Author

Submitted for the Froncort.AI Machine Learning Intern Assignment.