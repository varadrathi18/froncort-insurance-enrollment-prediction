# Insurance Enrollment Prediction + Outreach Assistant

## 1. Project Overview

The objective of this project was to build an end-to-end machine learning system capable of predicting whether an employee would enroll in a voluntary insurance plan and to develop an Outreach Assistant that helps the HR benefits team prioritize employees for outreach based on limited regional outreach capacity.

The project included data cleaning, feature engineering, model training, evaluation, and implementation of an agent with multiple tools.

---

# 2. Data Cleaning

The employee dataset and region profile dataset were merged using the **region** column.

Several data quality issues were identified and resolved.

## Cleaning performed

- Removed duplicate employee records according to the chosen duplicate-handling policy.
- Converted mixed-format dates into datetime format.
- Standardized inconsistent values in:
  - last_contact_channel
  - plan_tier_requested
  - broker_channel
- Correctly handled the sentinel value in prior_year_enrolled.
- Missing values were imputed where appropriate.
- Removed application_date and last_contact_date from the final model because they were not suitable predictive features after preprocessing.

---

# 3. Feature Engineering

Features were classified into three categories.

## Usable Features

- Salary
- Employment Type
- Region
- Has Dependents
- Tenure
- Previous Enrollment
- Plan Tier Requested
- Broker Channel
- Region Profile Features

## Analysis-only Features

- Employee ID
- Application Date
- Last Contact Date

## Forbidden / Leaky Features

- legacy_propensity_score

The legacy_propensity_score was excluded from the final model because it almost reconstructed the target and represented target leakage.

---

# 4. Fairness Considerations

Although demographic variables such as age, gender, and marital status were available, prediction explanations intentionally avoided referencing these attributes.

The Outreach Assistant also refuses to use legacy_propensity_score during prediction explanations.

This design improves transparency and avoids generating explanations based on sensitive demographic information.

---

# 5. Model Training

Two versions of each model were trained.

## Logistic Regression

- Without legacy_propensity_score
- With legacy_propensity_score

## Random Forest

- Without legacy_propensity_score
- With legacy_propensity_score

The Random Forest model without legacy_propensity_score was selected as the final model because it provided excellent performance while avoiding reliance on the leaky feature.

---

# 6. Model Evaluation

Evaluation metrics included:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- 5-Fold Cross Validation

The selected Random Forest model achieved approximately 99.9% cross-validation accuracy with very low variance across folds, demonstrating stable predictive performance.

---

# 7. Outreach Assistant

A rule-based agent was implemented with the following tools:

- predict_enrollment()
- lookup_region_profile()
- rank_outreach_candidates()
- explain_prediction()

The agent supports employee prediction, region lookup, outreach prioritization, and safe prediction explanations.

Two safety rules were enforced:

- Refusal to use legacy_propensity_score.
- Prediction explanations never reference age, gender, or marital status.

---

# 8. Limitations

- The dataset is synthetic.
- Region-level aggregate features may not generalize to real-world environments.
- No probability calibration was performed.
- The agent uses template-based explanations rather than an LLM.

---

# 9. Future Work

Future improvements could include:

- Probability calibration.
- SHAP-based explanations.
- Streamlit web application.
- LLM-powered conversational assistant.
- Real-time prediction API.

---

# 10. Conclusion

An end-to-end machine learning pipeline was successfully developed for insurance enrollment prediction. The final solution combines robust preprocessing, a high-performing Random Forest model, and an Outreach Assistant that supports HR teams while respecting leakage and fairness considerations.