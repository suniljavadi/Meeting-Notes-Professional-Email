import streamlit as st
from app.config.settings import get_settings
from app.models.schemas import EmailType, Tone
from app.services.pipeline import analyze_and_generate

st.set_page_config(page_title="Meeting to Email", page_icon="✉", layout="wide")
st.title("Meeting Notes → Professional Email")
st.caption("Synthetic transcripts only. Facts are extracted into a reviewable draft; nothing is sent automatically.")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "result" not in st.session_state:
    st.session_state.result = None

left, right = st.columns([1.05, 0.95])
with left:
    uploaded = st.file_uploader("Upload a TXT transcript", type=["txt"])
    if uploaded:
        st.session_state.transcript = uploaded.getvalue().decode("utf-8", errors="replace")
    transcript = st.text_area("Transcript", value=st.session_state.transcript, height=320, max_chars=30000)
    st.session_state.transcript = transcript
    email_type = st.selectbox("Email type", list(EmailType), format_func=lambda value: value.value)
    tone = st.selectbox("Tone", list(Tone), format_func=lambda value: value.value)
    if st.button("Analyze and generate", type="primary", use_container_width=True):
        if not transcript.strip():
            st.error("Enter a transcript first.")
        else:
            with st.spinner("Analyzing transcript..."):
                st.session_state.result = analyze_and_generate(transcript, get_settings(), email_type, tone)

with right:
    result = st.session_state.result
    if result:
        st.subheader("Analysis")
        st.write(result.analysis.summary)
        tab1, tab2, tab3 = st.tabs(["Actions", "Decisions", "Risks"])
        with tab1:
            for item in result.analysis.action_items:
                st.write(f"**{item.action}** | {item.owner} | {item.deadline} | {item.status.value}")
        with tab2:
            st.write(result.analysis.decisions or ["None identified"])
        with tab3:
            st.write(result.analysis.risks or ["None identified"])
        st.subheader("Copy-ready email")
        subject = st.text_input("Subject", result.email.subject)
        body = st.text_area("Edit email before sending", result.email.body, height=360)
        st.download_button("Download .txt", f"Subject: {subject}\n\n{body}", "meeting-follow-up.txt", use_container_width=True)
        if result.email.validation_passed:
            st.success("Validation passed")
        else:
            st.warning("Review warnings: " + "; ".join(result.email.validation_warnings))
    else:
        st.info("Your analysis and draft email will appear here.")
