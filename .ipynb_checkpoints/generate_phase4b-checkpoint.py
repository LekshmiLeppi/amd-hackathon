from pathlib import Path

files = {

"streamlit_app.py": '''
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
''',

"run_streamlit.sh": '''
streamlit run streamlit_app.py
''',

"run_streamlit.bat": '''
@echo off
streamlit run streamlit_app.py
pause
'''
}

for filepath, content in files.items():

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

print("=" * 50)
print("PHASE 4B GENERATED")
print("=" * 50)
print()
print("Run backend:")
print("uvicorn app.main:app --reload")
print()
print("Run frontend:")
print("streamlit run streamlit_app.py")