import streamlit as st
import requests
import base64
import io
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Google Lens-like Chatbot",
    page_icon="🔍",
    layout="wide"
)

# API Configuration
API_KEY = 'AIzaSyAVV....'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=' + API_KEY

def analyze_image_with_gemini(image_bytes, prompt="Describe what you see in this image in detail."):
    """Analyze image using Gemini API"""
    try:
        # Convert image to base64
        img_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Prepare payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_b64
                            }
                        }
                    ]
                }
            ]
        }
        
        # Make API request
        response = requests.post(API_URL, json=payload)
        
        if response.ok:
            result = response.json()
            # Extract the text response from Gemini
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            return "Analysis completed, but no text response found."
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def main():
    # Header
    st.title("🔍 Google Lens-like Chatbot")
    st.markdown("Upload an image and get AI-powered analysis using Gemini API")
    
    # Sidebar for additional options
    st.sidebar.header("Settings")
    
    # Custom prompt option
    custom_prompt = st.sidebar.text_area(
        "Custom Analysis Prompt",
        value="Describe what you see in this image in detail. Identify objects, text, people, and any interesting features.",
        height=100
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Upload an image to analyze"
    )
    
    # URL input option
    st.markdown("---")
    st.subheader("Or enter an image URL")
    image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
    
    # Process image
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            st.subheader("AI Analysis")
            
            # Show loading spinner
            with st.spinner("Analyzing image with Gemini..."):
                # Get image bytes
                image_bytes = uploaded_file.getvalue()
                
                # Analyze with Gemini
                analysis = analyze_image_with_gemini(image_bytes, custom_prompt)
                
                # Display results
                st.markdown("### Analysis Results:")
                st.write(analysis)
                
                # Add a copy button
                st.code(analysis, language="text")
    
    elif image_url:
        st.subheader("Image from URL")
        
        try:
            # Download image from URL
            response = requests.get(image_url)
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(image, caption="Image from URL", use_column_width=True)
                
                with col2:
                    st.subheader("AI Analysis")
                    
                    with st.spinner("Analyzing image with Gemini..."):
                        analysis = analyze_image_with_gemini(image_bytes, custom_prompt)
                        
                        st.markdown("### Analysis Results:")
                        st.write(analysis)
                        st.code(analysis, language="text")
            else:
                st.error(f"Failed to download image from URL. Status code: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error processing image URL: {str(e)}")
    
    # Instructions
    if not uploaded_file and not image_url:
        st.info("Upload an image or enter an image URL to get started!")
        
        # Example usage
        st.markdown("---")
        st.subheader("How to use:")
        st.markdown("""
        1. **Upload an image** using the file uploader above
        2. **Or enter an image URL** in the text field
        3. **Customize the analysis prompt** in the sidebar (optional)
        4. **View the AI analysis** results
        """)
        
        st.markdown("---")
        st.subheader("Features:")
        st.markdown("""
        - **Object Recognition**: Identify objects, people, and scenes
        - **Text Detection**: Read and extract text from images
        - **Labeling**: Get detailed descriptions and labels
        - **Conversational**: Ask specific questions about the image
        - **Customizable**: Modify analysis prompts for different use cases
        """)

if __name__ == "__main__":
    main() 