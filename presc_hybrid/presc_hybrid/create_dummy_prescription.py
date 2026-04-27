from PIL import Image, ImageDraw, ImageFont
import os

def create_prescription():
    # Create a white image
    img = Image.new('RGB', (600, 800), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a default font, otherwise use default
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        header_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()

    # Add Text
    d.text((200, 50), "Dr. John Doe, MD", fill=(0,0,0), font=header_font)
    d.text((50, 100), "Patient: Jane Smith", fill=(0,0,0), font=font)
    d.text((400, 100), "Date: 2023-10-27", fill=(0,0,0), font=font)
    
    d.text((50, 160), "Rx:", fill=(0,0,0), font=header_font)
    d.text((50, 200), "1. Amoxicillin 500mg", fill=(0,0,0), font=font)
    d.text((70, 230), "Take one capsule 3 times a day for 7 days.", fill=(0,0,0), font=font)
    
    d.text((50, 280), "2. Ibuprofen 400mg", fill=(0,0,0), font=font)
    d.text((70, 310), "Take one tablet every 6 hours as needed for pain.", fill=(0,0,0), font=font)
    
    d.text((50, 400), "Signature: ____________________", fill=(0,0,0), font=font)
    
    img.save("sample_prescription.jpg")
    print("Created sample_prescription.jpg")

if __name__ == "__main__":
    create_prescription()
