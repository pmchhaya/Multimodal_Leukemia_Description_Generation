import pdfplumber
import fitz
import os
import io
import argparse
from PIL import Image
import re

# Parse arguments from terminal 
parser=argparse.ArgumentParser(description="PDF Image Extractor")
parser.add_argument("input_file")
parser.add_argument("output_dir")
parser.add_argument("img_format")
parser.add_argument("img_quality")
args=parser.parse_args()

# Define  PDF file path
PDF_PATH = args.input_file
OUTPUT_IMAGES_DIR = args.output_dir
IMAGE_FORMAT = args.img_format.lower()  # Convert to lowercase
IMAGE_QUALITY = int(args.img_quality)

# Validate quality parameter
if IMAGE_QUALITY < 1 or IMAGE_QUALITY > 100:
    print(f"Warning: Quality {IMAGE_QUALITY} is invalid. Setting to 90.")
    IMAGE_QUALITY = 90

print(f"Using format: {IMAGE_FORMAT}, quality: {IMAGE_QUALITY}")

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_IMAGES_DIR):
    os.makedirs(OUTPUT_IMAGES_DIR)

# Removes all letters and unwanted characters from a string
def remove_letters(text):
    if not text:
        return "page"
    # Remove newlines, tabs, and other whitespace, then keep only numbers
    cleaned = re.sub(r'[^\w\s]', '', text.replace('\n', ' ').replace('\t', ' '))
    numbers_only = ''.join([c for c in cleaned if c.isdigit()])
    return numbers_only if numbers_only else "page"

# Resizes an image so that its width or height does not exceed the specified maximum size.
def resize_image(image):
    """
    Resizes an image so that its width or height does not exceed the specified maximum size.

    Args:
        image: The image to resize.

    Returns:
        The resized image.
    """

    # Calculate the maximum size as 70% of the larger side of the image.
    max_size = int(max(image.width, image.height) * 0.7)

    if image.width > max_size or image.height > max_size:
        if image.width > image.height:
            aspect_ratio = image.height / image.width
            new_width = max_size
            new_height = int(max_size * aspect_ratio)
        else:
            aspect_ratio = image.width / image.height
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        image = image.resize((new_width, new_height), Image.LANCZOS)
    return image

# Extracts and saves all images from the specified page of the document.
def save_images_from_page(document, page_number, product_reference):
    """
    Extracts and saves all images from the specified page of the document.

    Args:
        document: The PDF document.
        page_number: The page number to extract images from.
        product_reference: The product reference to use for the filenames of the saved images.

    Returns:
        A list of the filenames of the saved images.
    """

    saved_images = []
    pagina = document.load_page(page_number)
    imagens = pagina.get_images(full=True)

    for img_index, img in enumerate(imagens):
        xref = img[0]
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]

        # Convert bytes to Image and check size
        image = Image.open(io.BytesIO(image_bytes))
        if image.width < 500 or image.height < 500:
            continue

        # Resize the image
        image = resize_image(image)

        # Create a clean filename
        clean_reference = product_reference[:20] if len(product_reference) > 20 else product_reference
        if not clean_reference:
            clean_reference = "page"
        
        # Set the filename of the image and save
        image_filename = os.path.join(
            OUTPUT_IMAGES_DIR, f"{clean_reference}_{page_number + 1}_{img_index}.{IMAGE_FORMAT}")
        
        # Save with correct quality parameter (integer, not string)
        try:
            if IMAGE_FORMAT in ['jpg', 'jpeg']:
                image.save(image_filename, "JPEG", quality=IMAGE_QUALITY)
            elif IMAGE_FORMAT == 'png':
                image.save(image_filename, "PNG")
            else:
                # Default to JPEG for other formats
                image_filename = image_filename.replace(f'.{IMAGE_FORMAT}', '.jpg')
                image.save(image_filename, "JPEG", quality=IMAGE_QUALITY)
        except Exception as e:
            print(f"Error saving image: {e}")
            print(f"Format: {IMAGE_FORMAT}, Quality: {IMAGE_QUALITY}, Type: {type(IMAGE_QUALITY)}")
            continue

        saved_images.append(image_filename)

    return saved_images

# Opens the document with fitz 
document = fitz.open(PDF_PATH)

# Uses pdfplumber to extract text and fitz for images.
with pdfplumber.open(PDF_PATH) as pdf:
    pages = pdf.pages
    for index, pagina in enumerate(pages):
        # Extracts and prints text.
        texto = pagina.extract_text()
        print(f"Text on Page {index + 1}:")
        if texto:
            print(texto.strip())
        else:
            print("No text found on this page.")
        print("-" * 50)

        # Extracts and saves images.
        page_reference = remove_letters(texto) if texto else f"page_{index + 1}"
        imagens = save_images_from_page(document, index, page_reference)
        
        if imagens:
            for img in imagens:
                print(f"Image Saved: {img}")
        else:
            print("No images found on this page.")
        print("=" * 50)

document.close()