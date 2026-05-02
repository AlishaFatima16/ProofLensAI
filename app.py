import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG ---
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ProofLens AI", page_icon="🔍")
st.title("🔍 ProofLens AI")
st.caption("Multimodal Evidence Analyzer for Images & Claims")

# --- UI ---
uploaded_file = st.file_uploader("Upload an image (Screenshot, Product, or Scene)", type=["jpg", "jpeg", "png"])
user_claim = st.text_input("Or enter a claim to verify (Optional)")

if st.button("Analyze Evidence 🔥"):
    if uploaded_file or user_claim:
        with st.spinner("Analyzing reality..."):
            content = []
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            if user_claim:
                content.append(f"Analyze this claim: {user_claim}")

            # The "Secret Sauce" Instruction
            instruction = "Act as a forensic analyzer. Provide Observation, Concern, Recommendation, and Risk Level."
            content.insert(0, instruction)

            response = model.generate_content(content)

            st.divider()
            st.markdown(response.text)
    else:
        st.warning("Please provide an image or a text claim first!")
