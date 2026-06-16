
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Compliance Validator",
    layout="wide"
)

st.title("AI Compliance Audit Validator")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

if uploaded_file:

    with st.spinner("Analyzing document..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }

        response = requests.post(
            "http://localhost:8000/validate",
            files=files
        )

        result = response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Compliance Score",
                result.get(
                    "compliance_score",
                    0
                )
            )

        with col2:
            st.metric(
                "Risk Level",
                result.get(
                    "risk_level",
                    "UNKNOWN"
                )
            )

        with col3:
            st.metric(
                "Violations",
                result.get(
                    "violations",
                    0
                )
            )

        st.divider()

        st.subheader("Recommendations")

        for rec in result.get(
            "recommendations",
            []
        ):
            st.warning(rec)

        st.divider()

        st.subheader("Findings")

        findings = result.get(
            "findings",
            []
        )

        if findings:

            df = pd.DataFrame(findings)

            st.dataframe(
                df,
                use_container_width=True
            )

        if st.button(
            "Generate PDF Report"
        ):

            pdf_response = requests.post(
                "http://localhost:8000/report"
            )

            with open(
                "audit_report.pdf",
                "wb"
            ) as f:
                f.write(pdf_response.content)

            st.success(
                "Report downloaded."
            )
