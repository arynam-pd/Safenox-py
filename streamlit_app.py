import streamlit as st
from PIL import Image
import piexif
import io

def add_url_to_image_description(input_file, url):
    # Open the image from the file-like object
    img = Image.open(input_file)
    
    # Try loading existing EXIF or initialize a new one
    try:
        exif_dict = piexif.load(img.info["exif"])
    except (KeyError, piexif.InvalidImageDataError):
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    
    # Set the ImageDescription field with the URL (ASCII-encoded)
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = url.encode("ascii", "replace")
    
    # Convert EXIF dictionary to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save the image to a BytesIO object in JPEG format
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
        # Get the original filename and generate the output filename
        original_name = uploaded_file.name
        name = original_name.rsplit('.', 1)[0]
        output_name = f"{name}-1.jpg"
        
        # Process the image and get the output as a BytesIO object
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
