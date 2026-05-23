import google.generativeai as genai
import streamlit as st
from PIL import Image

# Configure API key
genai.configure(api_key="AIzaSyDA....")

# Use Gemini multimodal model for image + text
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_content(image, prompt):
    response = model.generate_content([image, prompt])
    return response.text

# Streamlit UI
st.title("Venu's LENS")
image = st.file_uploader("Upload the image", type=["png", "jpeg", "jpg"])
prompt = st.text_input("Enter the prompt")

if image and prompt:
    im = Image.open(image)
    st.image(im)
    st.write(generate_content(im, prompt))
