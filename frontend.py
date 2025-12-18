import streamlit as st
from rag_pipeline import extract_case_text, answer_query, llm_model

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=" AI Vakeel",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LAW-THEMED CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

/* REMOVE STREAMLIT DEFAULT BACKGROUND BLOCKS */
section[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
}

/* ================= COURTROOM-INSPIRED ANIMATED BACKGROUND ================= */
.stApp {
    background:
        linear-gradient(120deg, rgba(255,215,0,0.08), transparent 40%),
        linear-gradient(240deg, rgba(255,215,0,0.06), transparent 45%),
        radial-gradient(circle at top, rgba(255,255,255,0.06), transparent 35%),
        linear-gradient(135deg, #0a0f2c, #141b3d, #0a0f2c);
    background-size: 300% 300%;
    animation: courtMotion 22s ease-in-out infinite;
    font-family: 'Inter', sans-serif;
    color: #f5f5f5;
}

/* Smooth courtroom movement */
@keyframes courtMotion {
    0%   { background-position: 0% 50%; }
    25%  { background-position: 40% 60%; }
    50%  { background-position: 100% 50%; }
    75%  { background-position: 60% 40%; }
    100% { background-position: 0% 50%; }
}

/* ================= JUSTICE GLOW WAVES ================= */
.justice-wave {
    position: fixed;
    width: 120%;
    height: 120%;
    background: radial-gradient(circle, rgba(255,215,0,0.12), transparent 65%);
    animation: waveRotate 32s linear infinite;
    z-index: 0;
    pointer-events: none;
}

.justice-wave:nth-child(1) {
    top: -30%;
    left: -20%;
}

.justice-wave:nth-child(2) {
    bottom: -40%;
    right: -30%;
    animation-duration: 40s;
}

@keyframes waveRotate {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

/* ================= HERO ================= */
.hero {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(22px);
    border-radius: 26px;
    padding: 3rem 2rem;
    text-align: center;
    box-shadow: 0 30px 70px rgba(0,0,0,0.55);
    margin: 2.5rem 0 3rem 0;
    position: relative;
    z-index: 2;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    color: #ffd700;
}

.hero p {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    color: #eaeaff;
}

/* ================= CARDS ================= */
.card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(22px);
    border-radius: 22px;
    padding: 2.3rem;
    box-shadow: 0 22px 60px rgba(0,0,0,0.45);
    transition: all 0.35s ease;
    position: relative;
    z-index: 2;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 40px 90px rgba(255,215,0,0.35);
}

/* ================= FILE UPLOADER ================= */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    border: 1px dashed rgba(255,215,0,0.45);
}

/* ================= TEXT AREA ================= */
textarea {
    font-family: 'Inter', sans-serif !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
}

/* ================= BUTTON ================= */
.stButton>button {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(90deg, #ffcc33, #ffd700);
    color: #1b1b1b;
    font-weight: 700;
    border-radius: 14px;
    padding: 0.9rem 2.6rem;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 12px 35px rgba(255,215,0,0.45);
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 20px 60px rgba(255,215,0,0.75);
}

/* ================= RESPONSE ================= */
.response-box {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #1c1c44, #0e0e2a);
    border-left: 6px solid #ffd700;
    padding: 1.4rem;
    border-radius: 18px;
    margin-top: 1.2rem;
    animation: fadeUp 0.6s ease;
}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(16px);}
    to   {opacity: 1; transform: translateY(0);}
}

/* ================= FOOTER ================= */
.footer {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.85rem;
    color: #bbb;
    position: relative;
    z-index: 2;
}
</style>
""", unsafe_allow_html=True)

# ================= JUSTICE WAVES =================
st.markdown("""
<div class="justice-wave"></div>
<div class="justice-wave"></div>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">
    <h1>⚖️ AI Vakeel</h1>
    <p>Smart • Secure • Reliable — AI-powered FIR & Legal Case Analysis</p>
</div>
""", unsafe_allow_html=True)

# ================= MAIN CONTENT =================
col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.subheader("📄 Upload Your Case Report")
    uploaded_case = st.file_uploader("Upload FIR or legal report (PDF only)", type=["pdf"])

    case_context = ""
    if uploaded_case:
        with st.spinner("📚 Analyzing document..."):
            case_context = extract_case_text(uploaded_case)
        st.success("✅ Case uploaded successfully")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("💬 Ask Your Legal Question")
    user_query = st.text_area(
        "Enter your question",
        height=150,
        placeholder="E.g. What IPC sections apply and what punishment is prescribed?"
    )

    if st.button("🔍 Get Legal Advice"):
        if not uploaded_case:
            st.warning("⚠️ Upload a case report first")
        elif not user_query.strip():
            st.warning("⚠️ Enter a question")
        else:
            with st.spinner("🧠 AI analyzing the case..."):
                response = answer_query(user_query, case_context, llm_model)
            st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
⚖️ Developed with ❤️ by LegalAI • © 2025 AI Vakeel
</div>
""", unsafe_allow_html=True)
