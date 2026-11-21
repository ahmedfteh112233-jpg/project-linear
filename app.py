import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

from image_processing import (
    convert_to_grayscale,
    adjust_brightness,
    horizontal_flip,
    convert_to_black_white
)

st.set_page_config(
    page_title="MatrixVision",
    page_icon="🖼️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101426, #202b45);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    background: #c94f83;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🖼️ MatrixVision")
st.subheader("Professional Image Processing Studio")
st.write("Upload your image and transform it with powerful image processing tools.")

uploaded_file = st.file_uploader(
    "Upload Your Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    original = Image.open(uploaded_file).convert("RGB")
    image = np.array(original).copy()

    st.sidebar.title("Image Tools")

    operations = st.sidebar.multiselect(
        "Choose Operations",
        [
            "Grayscale",
            "Black & White",
            "Horizontal Flip",
            "Brightness"
        ]
    )

    brightness = st.sidebar.slider(
        "Brightness",
        -100,
        100,
        0
    )

    threshold = st.sidebar.slider(
        "Black & White Threshold",
        0,
        255,
        127
    )

    if "Grayscale" in operations:
        image = convert_to_grayscale(image)

    if "Black & White" in operations:
        image = convert_to_black_white(image, threshold)

    if "Horizontal Flip" in operations:
        image = horizontal_flip(image)

    if "Brightness" in operations:
        image = adjust_brightness(image, brightness)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(original, use_container_width=True)

    with col2:
        st.subheader("Processed Image")
        st.image(image, use_container_width=True)

    st.divider()

    output = BytesIO()
    Image.fromarray(image).save(output, format="PNG")

    st.download_button(
        "⬇️ Download Processed Image",
        data=output.getvalue(),
        file_name="MatrixVision_result.png",
        mime="image/png",
        use_container_width=True
    )

else:
    st.info("👆 Upload an image to start editing.")
