import streamlit as st
from rag_pipeline import extract_case_text, answer_query, llm_model

# Streamlit UI setup
st.set_page_config(page_title="⚖ AI Legal Advisor", layout="wide")
st.title("⚖ AI Legal Advisor – Case Report Assistant")

st.markdown("""
Welcome to *AI Legal Advisor*!  
Upload your FIR or case report, then ask questions like:
- "What sections are included in my FIR?"
- "What should I do next?"
- "Is this a bailable offence?"

The AI lawyer will analyze your case and provide helpful guidance.
""")


# --- Step 1: Case Report Upload ---
uploaded_case = st.file_uploader("📄 Upload your FIR or Case Report (PDF only):", type=["pdf"])

case_context = ""
if uploaded_case:
    with st.spinner("📚 Reading and analyzing your case report..."):
        case_context = extract_case_text(uploaded_case)
        st.success("✅ Case report uploaded successfully!")


# --- Step 2: Question Input ---
st.subheader("💬 Ask Your Legal Question")
user_query = st.text_area(
    "Enter your question below:",
    height=120,
    placeholder="Ask me...."
)


# --- Step 3: Generate Answer ---
if st.button("🔍 Get Legal Advice"):
    if not uploaded_case:
        st.warning("⚠ Please upload your case report first.")
    elif not user_query.strip():
        st.warning("⚠ Please enter a question.")
    else:
        with st.spinner("🧠 Analyzing your case and generating response..."):
            response = answer_query(user_query, case_context, llm_model)
        st.markdown("### 🧾 AI Lawyer’s Advice")
        st.success(response)
