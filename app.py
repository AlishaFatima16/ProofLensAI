import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ProofLens AI", 
    page_icon="🔍", 
    layout="centered"
)

# --- 2. API SETUP ---
# Ensure GEMINI_KEY is in your .streamlit/secrets.toml or Streamlit Cloud Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
except Exception:
    st.error("API Key not found. Please add GEMINI_KEY to your Streamlit secrets.")

# Using the 2.0-flash model as it's the current standard
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. UI DESIGN ---
st.title("🔍 ProofLens AI")
st.markdown("### *Multimodal Forensic Evidence Analyzer*")
st.write("Protect yourself from misinformation and hazards by analyzing images and claims together.")

st.divider()

# --- 4. INPUT SECTION ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📸 Visual Evidence")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], help="Upload screenshots, product photos, or scene images.")

with col2:
    st.markdown("#### ✍️ Textual Evidence")
    user_paste = st.text_area("Paste Claim", placeholder="Paste WhatsApp messages, news text, or links here...", height=150)

# --- 5. ANALYSIS LOGIC ---
if st.button("Start Forensic Analysis 🔥", use_container_width=True):
    if uploaded_file or user_paste:
        with st.spinner("🕵️ Investigator is analyzing the evidence..."):
            # Constructing the multimodal prompt
            content_parts = []
            
            # The "Secret Sauce" System Instruction
            system_instruction = """
            You are ProofLens AI, a professional forensic analyzer. 
            Analyze the provided evidence for authenticity, logic, and safety.
            If both image and text are provided, check if they contradict each other.
            
            Structure your response exactly as follows:
            🧠 **OBSERVATION**: [Objective description of what is seen/read]
            ⚠️ **CONCERN**: [Specific red flags, risks, or misleading elements]
            💡 **RECOMMENDATION**: [Clear, actionable steps for the user]
            🚦 **RISK LEVEL**: [Low / Medium / High / Critical]
            """
            content_parts.append(system_instruction)

            if uploaded_file:
                img = Image.open(uploaded_file)
                content_parts.append(img)
            
            if user_paste:
                content_parts.append(f"TEXT TO ANALYZE: {user_paste}")

            try:
                # Generate AI Response
                response = model.generate_content(content_parts)
                
                st.divider()
                st.subheader("📊 Forensic Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    else:
        st.warning("⚠️ Please provide an image or text evidence to begin.")

# --- 6. FOOTER ---
st.divider()
st.caption("Developed for #AISeekho2026 | Powered by Google Gemini 2.0")
