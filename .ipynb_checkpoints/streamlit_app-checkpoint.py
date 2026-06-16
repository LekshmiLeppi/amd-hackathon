import streamlit as st
import requests
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Compliance Dashboard",
    layout="wide",
    page_icon="🛡️"
)

API_URL = "http://127.0.0.1:8001"

# ----------------------------
# HEADER
# ----------------------------
st.title("🛡️ AI Compliance Audit Dashboard")
st.caption("Upload documents + optional rules for AI compliance analysis")

st.divider()

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("Backend Running (8001)")
    st.info("vLLM + FastAPI + Streamlit")

    st.markdown("---")
    st.subheader("📌 Supported Inputs")
    st.write("✔ PDF Document")
    st.write("✔ DOCX Document")
    st.write("✔ Optional Rules (TXT)")

# ----------------------------
# INPUTS
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Insurance Document",
        type=["pdf", "docx"]
    )

with col2:
    rules_file = st.file_uploader(
        "📜 Upload Rules (Optional)",
        type=["txt"]
    )

# ----------------------------
# PROCESSING
# ----------------------------
if uploaded_file:

    st.success(f"Document Uploaded: {uploaded_file.name}")

    if rules_file:
        st.success(f"Rules Uploaded: {rules_file.name}")

    with st.spinner("🧠 Running compliance analysis..."):

        try:
            # ----------------------------
            # SEND FILES TO BACKEND
            # ----------------------------
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            if rules_file:
                files["rules"] = (
                    rules_file.name,
                    rules_file.getvalue(),
                    "text/plain"
                )

            response = requests.post(
                f"{API_URL}/validate",
                files=files,
                timeout=120
            )

            if response.status_code != 200:
                st.error(f"Backend Error: {response.text}")
                st.stop()

            result = response.json()

            # ----------------------------
            # METRICS
            # ----------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📊 Compliance Score", result.get("compliance_score", 0))

            with col2:
                risk = result.get("risk_level", "UNKNOWN")

                if risk == "HIGH":
                    st.error("🔴 HIGH RISK")
                elif risk == "MEDIUM":
                    st.warning("🟠 MEDIUM RISK")
                else:
                    st.success("🟢 LOW RISK")

            with col3:
                st.metric("🚨 Violations", result.get("violations", 0))

            st.divider()

            # ----------------------------
            # RULE SUMMARY
            # ----------------------------
            st.subheader("📜 Rule Summary")

            colA, colB, colC = st.columns(3)

            colA.info(f"Total Rules: {result.get('total_rules', 0)}")
            colB.success(f"System Rules: {result.get('system_rules', 0)}")
            colC.warning(f"User Rules: {result.get('user_rules', 0)}")

            st.divider()

            # ----------------------------
            # RECOMMENDATIONS
            # ----------------------------
            st.subheader("💡 Recommendations")

            recommendations = result.get("recommendations", [])

            if recommendations:
                for rec in recommendations:
                    st.warning(f"⚠️ {rec}")
            else:
                st.success("No major compliance issues detected.")

            st.divider()

            # ----------------------------
            # FINDINGS TABLE
            # ----------------------------
            st.subheader("📋 Detailed Findings")

            findings = result.get("findings", [])

            if isinstance(findings, list) and len(findings) > 0:

                cleaned = []
                for f in findings:
                    cleaned.append({
                        "Rule": f.get("rule", ""),
                        "Status": f.get("status", ""),
                        "Confidence": float(f.get("confidence", 0)),
                        "Evidence": f.get("evidence", ""),
                        "Reason": f.get("reason", "")
                    })

                df = pd.DataFrame(cleaned)
                st.dataframe(df, use_container_width=True)

            else:
                st.info("No findings generated.")

            st.divider()

            # ----------------------------
            # REPORT DOWNLOAD (FIXED)
            # ----------------------------
            st.subheader("📄 Report")

            if st.button("⬇️ Download PDF Report"):

                with st.spinner("Generating report..."):

                    pdf_response = requests.post(
                        f"{API_URL}/report",
                        timeout=120
                    )

                    if pdf_response.status_code == 200:

                        # 🔥 NO FILE SAVE — DIRECT DOWNLOAD
                        st.download_button(
                            label="Click to Download Report",
                            data=pdf_response.content,
                            file_name="audit_report.pdf",
                            mime="application/pdf"
                        )

                    else:
                        st.error("Failed to generate report")

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend not reachable. Start FastAPI on port 8001.")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# ----------------------------
# FOOTER
# ----------------------------
st.divider()
st.caption("🚀 AI Compliance System | Streamlit + FastAPI + vLLM")