# Insurance Enrollment Prediction + Outreach Assistant

## 1. Project Overview

This project was completed as part of the **Froncort.AI Machine Learning Intern Assignment**.

The objective was to develop an end-to-end machine learning solution capable of predicting whether an employee would enroll in a voluntary insurance plan and to design an Outreach Assistant that helps HR teams prioritize employees for outreach when outreach capacity is limited.

The project covers the complete machine learning workflow, including data understanding, preprocessing, feature engineering, model development, evaluation, and the implementation of a tool-based assistant with responsible AI safeguards.

---

# 2. Dataset Overview

Two datasets were provided:

- **Employee Dataset:** Contains employee demographic, employment, enrollment, and communication information.
- **Region Benefit Profile Dataset:** Contains region-level operational statistics such as historical enrollment rate, average salary, average premium cost, broker rating, and available HR outreach capacity.

These datasets were merged using the **region** attribute to create the final modeling dataset.

---

# 3. Data Cleaning

Several data quality issues were identified before model development.

The following preprocessing steps were performed:

- Removed duplicate employee records according to the selected duplicate-handling policy.
- Converted mixed-format date columns into a consistent datetime format.
- Standardized inconsistent categorical values for:
  - `last_contact_channel`
  - `plan_tier_requested`
  - `broker_channel`
- Correctly handled sentinel values in `prior_year_enrolled`.
- Imputed missing values where appropriate.
- Merged employee records with regional profile information.
- Removed `application_date` and `last_contact_date` from the final model after extracting any useful information, as raw dates are not directly suitable for prediction.

These preprocessing steps produced a clean and consistent dataset for model training.

---

# 4. Feature Engineering

Features were categorized according to their intended use.

## Modeling Features

Examples include:

- Salary
- Employment Type
- Region
- Has Dependents
- Tenure
- Prior Year Enrollment
- Plan Tier Requested
- Broker Channel
- Historical Enrollment Rate
- Average Salary (Region)
- Average Premium Cost
- Broker Rating
- HR Outreach Capacity
- Enrollment Window

## Analysis-Only Features

The following features were retained for identification or reporting but excluded from model training:

- Employee ID
- Application Date
- Last Contact Date

## Target Leakage

The dataset contained the feature:

- `legacy_propensity_score`

This feature was identified as a leakage feature because it almost reconstructed the target variable. Including it would produce unrealistically high predictive performance while reducing the model's ability to generalize.

Therefore, this feature was excluded from the final production model and the Outreach Assistant explicitly refuses to use it for predictions or explanations.

---

# 5. Fairness Considerations

Although demographic variables such as **age**, **gender**, and **marital status** were available in the dataset, prediction explanations intentionally avoid referencing these attributes.

This design decision was taken to produce explanations based on operational and employment-related factors rather than protected demographic characteristics.

The Outreach Assistant also refuses any request to explain predictions using `legacy_propensity_score`, ensuring that explanations remain both fair and free from target leakage.

---

# 6. Model Development

Two machine learning algorithms were evaluated:

- Logistic Regression
- Random Forest Classifier

For each algorithm, two versions were trained:

- Model excluding `legacy_propensity_score`
- Model including `legacy_propensity_score` (used only to demonstrate leakage)

Training followed a stratified train-test split, and performance was validated using 5-fold cross-validation.

The Random Forest model trained **without** the leakage feature was selected as the final deployment model because it provided strong predictive performance while maintaining realistic generalization.

---

# 7. Model Evaluation

Model performance was evaluated using multiple complementary metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Confusion Matrix
- 5-Fold Cross Validation

To provide meaningful context, two baseline approaches were also implemented:

- Majority Class Baseline
- Rule-Based Baseline (Dependents Rule)

The final Random Forest model outperformed both baseline approaches across the primary evaluation metrics.

Since the project focuses on outreach prioritization, a business-oriented evaluation metric was also included.

### Precision@K

Precision@50, Precision@100, and Precision@200 were calculated to measure how accurately the highest-ranked employees were identified for outreach.

The model achieved excellent Precision@K performance, demonstrating its suitability for prioritizing limited HR outreach resources.

---

# 8. Outreach Assistant

A rule-based Outreach Assistant was developed to expose the trained model through four tools.

## 1. predict_enrollment()

Predicts whether an employee is likely to enroll and returns:

- Prediction
- Probability
- Confidence Level

## 2. lookup_region_profile()

Returns operational information for a selected region, including:

- Historical enrollment rate
- Average salary
- Average premium cost
- Broker rating
- Outreach capacity
- Enrollment window

## 3. rank_outreach_candidates()

Ranks employees within a selected region according to predicted enrollment probability and returns only the highest-priority employees that can realistically be contacted based on regional HR outreach capacity.

## 4. explain_prediction()

Generates a natural-language explanation describing the primary operational factors influencing an employee's prediction.

The explanation intentionally excludes:

- Age
- Gender
- Marital Status
- `legacy_propensity_score`

to satisfy fairness and leakage requirements.

---

# 9. Responsible AI Considerations

Several safeguards were incorporated into the final system.

- The final production model excludes the identified leakage feature.
- The Outreach Assistant refuses requests involving `legacy_propensity_score`.
- Prediction explanations avoid protected demographic attributes.
- Business-oriented metrics (Precision@K) were used alongside traditional classification metrics to better reflect real-world deployment requirements.

---

# 10. Limitations

This project has several limitations.

- The dataset is synthetic and may not capture all characteristics of real employee populations.
- Regional aggregate statistics may not generalize across organizations.
- Model probabilities were not calibrated.
- Prediction explanations are template-based and do not provide feature attribution at the model level.

---

# 11. Future Improvements

Possible future enhancements include:

- Probability calibration.
- SHAP-based feature attribution.
- Streamlit-based interactive web application.
- REST API deployment.
- LLM-powered conversational HR assistant.
- Continuous model retraining using new enrollment data.

---

# 12. Conclusion

This project successfully demonstrates the complete lifecycle of a machine learning solution, from raw data processing to deployment-oriented decision support.

The final solution combines robust preprocessing, feature engineering, comprehensive model evaluation, business-oriented ranking metrics, and a responsible Outreach Assistant capable of supporting HR teams while respecting fairness and target leakage constraints.