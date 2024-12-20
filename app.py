import os
import streamlit as st
from vision_agent.agent.vision_agent_coder_v2 import VisionAgentCoderV2
from PIL import Image, UnidentifiedImageError
import tempfile
from pathlib import Path

# Set API Keys (Replace with your actual keys)

# os.environ["OPENAI_API_KEY"] = "------"
# os.environ["ANTHROPIC_API_KEY"] = "-----"


# Initialize the Vision Agent
agent = VisionAgentCoderV2(verbose=True)

# Streamlit app configuration
st.set_page_config(page_title="Vision Agent App", layout="wide")

# Sidebar: Project Description
with st.sidebar:
    st.title("Vision Agent Project")
    st.markdown("""
    **Vision Agent** is an advanced AI-powered tool to perform visual understanding tasks.

    This app allows users to:
    - Upload an image for analysis.
    - Provide queries for vision-based tasks.
    - View AI-generated results and visualizations.
    
    Explore the power of Vision Agent for real-world applications!
    """)

# Main section: Input and Output
st.header("Agentic AI - Vision Agent for Image Understanding")
st.subheader("AI Agents that Plan, Reason, and Act")

# File uploader for image input
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    try:
        # Display the uploaded image
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_container_width=False)
    except UnidentifiedImageError:
        st.error("Invalid image file. Please upload a valid JPG/PNG image.")

# User query input
user_query = st.text_input("Enter your query", placeholder="e.g., Count the total number of people in this image.")

# Submit button
if st.button("Submit"):
    if uploaded_image and user_query:
        try:
            # Save the uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file_path = temp_file.name
                img.save(temp_file_path, format="JPEG")

            # Verify the saved image
            with Image.open(temp_file_path) as img:
                img.verify()  # Ensure integrity of the file

            # Process the image using the Vision Agent
            with st.spinner("Processing your request..."):
                response = agent(user_query, media=Path(temp_file_path))  # Pass the file path as a Path object

            # Display the results
            st.markdown("### **Query Result:**")
            st.text_area("Response", value=response, height=500)

        except Exception as e:
            st.error(f"An error occurred: {e}")
