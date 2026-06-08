import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="RetinaScan AI", layout="centered")

st.title("Diabetic Retinopathy Screening System")
st.write("Upload high-resolution fundus retinal image files to evaluate status.")

API_ENDPOINT = "http://api-service:8000/api/v1/predict"

uploaded_file = st.file_uploader("Choose a retinal image source files...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Retinal Scan File Location Preview", use_container_width=True)
    
    if st.button("Analyze Scan Structure"):
        with st.spinner("Executing Network Core Evaluator Protocols..."):
            # Prepare memory footprint payload stream
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            files = {"file": (uploaded_file.name, img_byte_arr, f"image/{uploaded_file.type}")}
            
            try:
                response = requests.post(API_ENDPOINT, files=files, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Analysis Complete!")
                    st.subheader(f"Diagnosis: **{data['diagnosis']}**")
                    st.progress(data['confidence'])
                    st.write(f"Model Inference Confidence score rating value matches: **{data['confidence']*100:.2f}%**")
                    
                    if data['class_id'] > 0:
                        st.warning("Attention: Medical signs of clinical retinopathy detected. Prompt validation suggested.")
                else:
                    st.error(f"Error calling backend routing api pipeline: Status Code {response.status_code}")
            except Exception as e:
                st.error(f"Failed to communicate with API service infrastructure connection node: {e}")
