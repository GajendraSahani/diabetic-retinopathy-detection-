import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="RetinaScan AI Engine Room", layout="wide")

st.title("Deep Learning Diagnostic Interface for Retinopathy")
st.write("Production pipeline directly coupled via REST API instances to your trained Keras graph models.")

BACKEND_ENDPOINT = "http://api-service:8000/api/v1/predict"

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Data Input Stream")
    uploaded_scan = st.file_uploader("Upload Retinal Fundus File Image...", type=["png", "jpg", "jpeg"])
    if uploaded_scan:
        opened_image = Image.open(uploaded_scan)
        st.image(opened_image, caption="Uploaded Eye Scan Payload Target Preview", use_container_width=True)

with right_col:
    st.subheader("Model Diagnostics Engine")
    if uploaded_scan and st.button("Trigger Deep Learning Inference"):
        with st.spinner("Processing through your model's neural network components..."):
            byte_buffer = io.BytesIO()
            opened_image.save(byte_buffer, format='JPEG')
            binary_payload = byte_buffer.getvalue()
            
            files_multipart = {"file": (uploaded_scan.name, binary_payload, "image/jpeg")}
            
            try:
                api_response = requests.post(BACKEND_ENDPOINT, files=files_multipart, timeout=45)
                if api_response.status_code == 200:
                    json_data = api_response.json()
                    
                    st.success("Inference Evaluator Protocol Succeeded.")
                    st.metric(label="Predicted Condition Status Class", value=json_data['diagnosis'])
                    st.metric(label="Network Probability Output Confidence Match", value=f"{json_data['confidence']*100:.2f}%")
                    
                    # Highlight clinical status warnings depending on output class indexing thresholds
                    if json_data['class_id'] >= 2:
                        st.error("Clinical Severity Flag: Referral for clinical verification strongly recommended.")
                    elif json_data['class_id'] == 1:
                        st.warning("Warning Flag: Early signs of mild condition detected. Regular screening advised.")
                else:
                    st.error(f"API Error. Status Code: {api_response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to the API container: {e}")
