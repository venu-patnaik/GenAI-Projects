import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDAzSKPwxts...")  #Replace with your Gemini API key

# Load multimodal model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define function to get AI explanation
def get_explanation(image, question):
    try:
        response = model.generate_content([image, question])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App UI
st.set_page_config(page_title="AI Tutor", layout="centered")
st.title("AI Tutor – Learn with Images")

uploaded_img = st.file_uploader("Upload your question/diagram (PNG, JPEG)", type=["png", "jpg", "jpeg"])
user_prompt = st.text_area("Ask your question based on the image")

if uploaded_img and user_prompt:
    image = Image.open(uploaded_img)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Thinking..."):
        result = get_explanation(image, user_prompt)

    st.markdown("### AI Explanation")
    st.write(result)

st.markdown("---")
st.caption("Powered by Gemini Pro Vision · Developed by Venu")
