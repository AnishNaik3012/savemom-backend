import io
from PIL import Image
import pypdf

def load_image(file_bytes: bytes) -> Image.Image:
    """Load bytes into a PIL Image."""
    return Image.open(io.BytesIO(file_bytes))

def load_pdf_images(file_bytes: bytes) -> list[Image.Image]:
    """Convert PDF pages to images (using pypdf to extract if possible, or simple placeholder for text extraction).
    Note: For true PDF-to-Image rendering without external system dependencies like poppler, 
    we might need to rely on Gemini's direct PDF handling or a pure python library.
    
    FOR EXTRACTING TEXT: pypdf is great.
    FOR EXTRACTING IMAGES FOR VISION MODELS: It's harder without poppler.
    
    Simpler approach for this module: 
    - If it's a PDF, we extract text and try to extract embedded images.
    - OR we just pass the PDF bytes to Gemini if it supports it directly (Gemini 1.5 Pro does).
    
    For this 'ready-to-integrate' module, let's assume valid image input for now, 
    or basic text extraction for PDFs.
    """
    images = []
    # Simplified: extracting embedded images from PDF
    # In a real production environment, you'd use pdf2image (requires poppler)
    
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            for image_file_object in page.images:
                images.append(Image.open(io.BytesIO(image_file_object.data)))
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        
    return images

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF."""
    text = ""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text
