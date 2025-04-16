import streamlit as st
from PIL import Image
import piexif
import io

def add_url_to_image_description(input_file, url):
    # Open the uploaded image
    img = Image.open(input_file)
    
    # Check and convert image mode if necessary
    if img.mode not in ['L', 'RGB', 'CMYK']:
        img = img.convert('RGB')  # Convert to RGB to ensure JPEG compatibility
    
    # Handle EXIF data
    try:
        exif_dict = piexif.load(img.info["exif"])
    except (KeyError, piexif.InvalidImageDataError):
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = url.encode("ascii", "replace")
    exif_bytes = piexif.dump(exif_dict)
    
    # Save the image to a BytesIO object
    output_file = io.BytesIO()
    img.save(output_file, format="JPEG", exif=exif_bytes)
    output_file.seek(0)
    return output_file

# Streamlit app interface
st.title("Embed URL in Image EXIF Metadata")
st.write("Upload an image and enter a URL to embed in its EXIF metadata.")

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

# Text input for URL
url = st.text_input("Enter the URL to embed")

# Process the image when the button is clicked
if uploaded_file and url:
    if st.button("Process"):
        # Generate output filename based on the original
        original_name = uploaded_file.name
        name = original_name.rsplit('.', 1)[0]
        output_name = f"{name}-1.jpg"
        
        # Process the image
        processed_image = add_url_to_image_description(uploaded_file, url)
        
        # Provide a download button for the processed image
        st.download_button(
            label="Download processed image",
            data=processed_image,
            file_name=output_name,
            mime="image/jpeg"
        )
        st.success(f"Image processed successfully. Download the file: {output_name}")



# img = Image.open("test_unsafe.jpg")
# exif = piexif.load(img.info["exif"])
# print(exif["0th"][piexif.ImageIFD.ImageDescription].decode())
