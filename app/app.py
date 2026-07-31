import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from src.assistant import (
    predict_enrollment,
    lookup_region_profile,
    rank_outreach_candidates,
    explain_prediction,
)

st.set_page_config(
    page_title="Insurance Outreach Assistant",
    page_icon="🏥",
    layout="wide",
)

with st.sidebar:

    st.title("🏥 Froncort")

    st.markdown("---")

    st.write("### Project")

    st.write("""
AI-powered insurance enrollment prediction system.

Features:

- Predict enrollment
- Region analytics
- Outreach ranking
- Explainable AI
""")

    st.markdown("---")

    st.success("Model Ready")

st.title("🏥 Insurance Enrollment Outreach Assistant")

st.caption(
    "AI-powered decision support system for predicting insurance enrollment "
    "and assisting HR outreach teams."
)

st.divider()
# st.markdown(
#     "Predict employee enrollment, explore regional profiles, rank outreach candidates, "
#     "and generate explainable predictions."
# )

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Predict Enrollment",
    "🌍 Region Profile",
    "📋 Outreach Ranking",
    "💡 Explain Prediction",
])
with tab1:

    st.subheader("📈 Predict Employee Enrollment")

    employee_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1,
        key="predict_id",
    )

    if st.button("Predict Enrollment", use_container_width=True):

        result = predict_enrollment(employee_id)

        st.write(result)
        st.stop()

        if isinstance(result, dict) and "Error" in result:
            st.error(result["Error"])

        elif isinstance(result, dict):

            prediction = result["Prediction"]

            if prediction == "Likely to Enroll":
                st.success("✅ Likely to Enroll")
            else:
                st.warning("⚠️ Unlikely to Enroll")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Probability",
                    result["Probability"],
                )

            with col2:
                st.metric(
                    "Confidence",
                    result["Confidence"],
                )

        else:
            st.error("Unexpected response received.")

with tab2:

    st.subheader("🌍 Region Benefit Profile")

    region = st.selectbox(
        "Select Region",
        [
            "West",
            "South",
            "Northeast",
            "Midwest",
        ],
    )

    if st.button("Show Region Profile", use_container_width=True):

        profile = lookup_region_profile(region)

        if isinstance(profile, dict) and "Error" in profile:
            st.error(profile["Error"])

        elif isinstance(profile, dict):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Average Salary",
                    profile.get("Average Salary", "N/A")
                )

                st.metric(
                    "Historical Enrollment",
                    profile.get("Historical Enrollment Rate", "N/A")
                )

                st.metric(
                    "Average Premium",
                    profile.get("Average Premium Cost", "N/A")
                )

            with col2:

                st.metric(
                    "Broker Rating",
                    profile.get("Benefits Broker Rating", "N/A")
                )

                st.metric(
                    "HR Capacity",
                    profile.get("HR Outreach Capacity", "N/A")
                )

                st.metric(
                    "Enrollment Window",
                    profile.get("Open Enrollment Window (Days)", "N/A")
                )

        else:
            st.error("Unexpected response received.")

with tab3:

    st.subheader("📋 Top Outreach Candidates")

    region = st.selectbox(
        "Region",
        [
            "West",
            "South",
            "Northeast",
            "Midwest",
        ],
        key="ranking",
    )

    if st.button("Generate Ranking", use_container_width=True):

        ranking = rank_outreach_candidates(region)

        if isinstance(ranking, dict):

            st.error(ranking.get("Error", "Unable to generate ranking."))

        else:

            st.dataframe(
                ranking,
                use_container_width=True,
                hide_index=True,
            )

            csv = ranking.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Download Ranking",
                csv,
                "outreach_candidates.csv",
                "text/csv",
                use_container_width=True,
            )

with tab4:

    st.subheader("💡 Prediction Explanation")

    employee_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1,
        key="explain",
    )

    if st.button("Explain Prediction", use_container_width=True):

        explanation = explain_prediction(employee_id)
        st.write(explanation)
        st.stop()

        if isinstance(explanation, dict) and "Error" in explanation:
            st.error(explanation["Error"])

        elif isinstance(explanation, dict):

            prediction = explanation["Prediction"]

            if prediction == "Likely to Enroll":
                st.success("✅ Likely to Enroll")
            else:
                st.warning("⚠️ Unlikely to Enroll")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Probability",
                    explanation["Probability"],
                )

            with col2:
                st.metric(
                    "Confidence",
                    explanation["Confidence"],
                )

            st.subheader("Explanation")

            st.info(explanation["Explanation"])

        else:
            st.error("Unexpected response received.")

st.divider()

st.caption(
    "Developed using Streamlit • Scikit-learn • Pandas"
)