import pandas as pd
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

df = pd.read_csv(DATA_DIR / "employees_final.csv")

employees = pd.read_csv(DATA_DIR / "employees_final.csv")

predictions = pd.read_csv(DATA_DIR / "predictions.csv")

employee_predictions = employees.merge(
    predictions,
    on="employee_id",
    how="inner"
)

region_df = pd.read_csv(DATA_DIR / "region_benefit_profiles.csv")

model = joblib.load(MODEL_DIR / "final_model.pkl")

def predict_enrollment(employee_id):
    employee = employee_predictions[
        employee_predictions["employee_id"] == employee_id
    ]

    if employee.empty:
        return {
            "Status": "Error",
            "Message": "Employee not found."
        }

    probability = float(employee["predicted_probability"].iloc[0])
    prediction = int(employee["predicted_enrollment"].iloc[0])

    # Confidence level
    if probability >= 0.90 or probability <= 0.10:
        confidence = "High"
    elif probability >= 0.70 or probability <= 0.30:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "Employee ID": int(employee_id),
        "Prediction": "Likely to Enroll" if prediction == 1 else "Not likely to Enroll",
        "Probability": f"{probability:.2%}",
        "Confidence": confidence
    }


def rank_outreach_candidates(region):
    region_info = region_df[
        region_df["region"].str.lower() == region.lower()
    ]

    if region_info.empty:
        return {
            "Status": "Error",
            "Message": "Region not found."
        }

    capacity = int(region_info["hr_outreach_capacity"].iloc[0])

    region_employees = employee_predictions[
        employee_predictions["region"].str.lower() == region.lower()
    ].copy()

    ranked = (
        region_employees
        .sort_values("predicted_probability", ascending=False)
        .head(capacity)
        .copy()
    )

    ranked["Rank"] = range(1, len(ranked) + 1)

    ranked["Probability"] = (
        ranked["predicted_probability"] * 100
    ).round(2).astype(str) + "%"

    ranked["Prediction"] = ranked["predicted_enrollment"].map({
        1: "Likely to Enroll",
        0: "Unlikely to Enroll"
    })

    print(f"\nRegion : {region.title()}")
    print(f"HR Outreach Capacity : {capacity}")
    print(f"Employees Recommended : {len(ranked)}\n")

    return ranked[
        [
            "Rank",
            "employee_id",
            "Probability",
            "Prediction"
        ]
    ]

def lookup_region_profile(region):
    region_info = region_df[
        region_df["region"].str.lower() == region.lower()
    ]

    if region_info.empty:
        return {
            "Status": "Error",
            "Message": "Region not found."
        }

    region_info = region_info.iloc[0]

    return {
        "Region": region_info["region"],
        "Average Salary": f"${region_info['avg_salary_region']:,.2f}",
        "Historical Enrollment Rate": f"{region_info['hist_enrollment_rate_region']:.2%}",
        "Average Premium Cost": f"${region_info['avg_premium_cost_usd']:,.2f}",
        "Benefits Broker Rating": float(round(region_info["benefits_broker_rating"], 2)),
        "HR Outreach Capacity": int(region_info["hr_outreach_capacity"]),
        "Open Enrollment Window (Days)": int(region_info["open_enrollment_window_days"])
    }

def explain_prediction(employee_id, requested_features=None):
    """
    Generates a safe, natural-language explanation for an employee's prediction.
    """

    employee = employee_predictions[
        employee_predictions["employee_id"] == employee_id
    ]

    if employee.empty:
        return {
            "Status": "Error",
            "Message": "Employee not found."
        }

    # Refusal rule
    if requested_features is not None:
        forbidden = {"legacy_propensity_score"}

        if any(feature in forbidden for feature in requested_features):
            return {
                "Status": "Refused",
                "Reason": (
                    "The feature 'legacy_propensity_score' was identified as a "
                    "target leakage feature and cannot be used for prediction "
                    "or explanation."
                )
            }

    employee = employee.iloc[0]

    probability = float(employee["predicted_probability"])
    prediction = int(employee["predicted_enrollment"])

    # -----------------------
    # Confidence
    # -----------------------

    if probability >= 0.90 or probability <= 0.10:
        confidence = "High"
    elif probability >= 0.70 or probability <= 0.30:
        confidence = "Medium"
    else:
        confidence = "Low"

    # -----------------------
    # Build explanation
    # -----------------------

    positive_factors = []
    negative_factors = []

    # Salary
    if employee["salary"] >= employee_predictions["salary"].median():
        positive_factors.append("the employee has an above-average salary")
    else:
        negative_factors.append("the employee has a below-average salary")

    # Dependents
    if employee["has_dependents"] == "Yes":
        positive_factors.append("the employee has dependents")
    else:
        negative_factors.append("the employee has no dependents")

    # Tenure
    if employee["tenure_years"] >= 10:
        positive_factors.append("the employee has long tenure with the company")
    elif employee["tenure_years"] <= 2:
        negative_factors.append("the employee is relatively new to the organization")

    # Previous enrollment
    if employee["prior_year_enrolled"] == "Yes":
        positive_factors.append("the employee enrolled in the previous year")
    else:
        negative_factors.append("the employee has no previous enrollment history")

    # Employment type
    if employee["employment_type"] == "Full-Time":
        positive_factors.append("the employee works full-time")

    # Region
    if employee["hist_enrollment_rate_region"] >= 0.70:
        positive_factors.append("the employee belongs to a region with historically high enrollment")
    elif employee["hist_enrollment_rate_region"] <= 0.40:
        negative_factors.append("the employee belongs to a region with relatively low enrollment")

    # Enrollment window
    if employee["open_enrollment_window_days"] >= 20:
        positive_factors.append("there is sufficient time remaining in the enrollment window")

    # Plan tier
    if employee["plan_tier_requested"] != "Unknown":
        positive_factors.append(
            f"the requested plan tier is {employee['plan_tier_requested']}"
        )

    # -----------------------
    # Natural-language explanation
    # -----------------------

    if prediction == 1:

        explanation = (
            f"This employee is predicted to enroll with a probability of "
            f"{probability:.0%}. The prediction is primarily supported because "
            f"{', '.join(positive_factors[:3])}."
        )

        if negative_factors:
            explanation += (
                f" Although {', '.join(negative_factors[:2])}, "
                f"the overall combination of employment and regional factors "
                f"still indicates a high likelihood of enrollment."
            )

    else:

        explanation = (
            f"This employee is predicted not to enroll with a probability of "
            f"{1-probability:.0%}. The prediction is primarily influenced because "
            f"{', '.join(negative_factors[:3])}."
        )

        if positive_factors:
            explanation += (
                f" While {', '.join(positive_factors[:2])}, "
                f"these positive factors were not sufficient to outweigh the "
                f"overall prediction."
            )

    explanation += (
        "\n\nAge, gender, marital status, and "
        "legacy_propensity_score were intentionally excluded from this "
        "explanation to satisfy the project's fairness and leakage requirements."
    )

    return {
        "Employee ID": int(employee_id),
        "Prediction": (
            "Likely to Enroll"
            if prediction == 1
            else "Not Likely to Enroll"
        ),
        "Probability": f"{probability:.2%}",
        "Confidence": confidence,
        "Explanation": explanation
    }