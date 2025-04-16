from PIL import Image
import piexif

def add_url_to_image_description(image_path, output_path, url):
    img = Image.open(image_path)

    # Try loading existing EXIF or initialize new one
    try:
        exif_dict = piexif.load(img.info["exif"])
    except (KeyError, piexif.InvalidImageDataError):
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Set the ImageDescription field (ASCII, not UTF-8!)
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = url.encode("ascii", "replace")

    # Dump and save with new EXIF
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, exif=exif_bytes)
    print(f"✅ URL embedded in EXIF metadata: {output_path}")

# Example usage
add_url_to_image_description("Unsafe1.webp", "test_unsafe1.webp", "http://malicious.example.com")



# img = Image.open("test_unsafe.jpg")
# exif = piexif.load(img.info["exif"])
# print(exif["0th"][piexif.ImageIFD.ImageDescription].decode())
