# home/utils.py

import os
from PIL import Image
# NOTE: If you decide to implement advanced stamp detection, you will need 
# 'import cv2' and 'import numpy as np' here, and you must install opencv-python.

def validate_prescription_stamp(file_path):
    """
    Performs a simulated validation check for a doctor's stamp.

    For a real-world implementation, this function would use:
    1. Computer Vision (OpenCV) for template matching or feature detection.
    2. OCR (Tesseract/pytesseract) to read and verify registration numbers/names.
    
    Current Logic (Placeholder/Simulation):
    - Tries to open the image to check if it's a valid image file.
    - **SIMULATES** stamp detection by returning True (Valid) 
      if the filename contains the word 'stamp' (case-insensitive) for testing.
    - Otherwise returns False (Fake/No Stamp).

    Returns:
    - True: Stamp detected (Valid)
    - False: Stamp not detected (Fake/Invalid)
    - "error": Processing failed (e.g., corrupted file, not an image/PDF)
    """
    
    # 1. Check if the file is a PDF (we skip stamp validation for PDFs as it's complex)
    if file_path.lower().endswith('.pdf'):
        # For simplicity, we assume PDFs from clinics are pre-validated or handled manually.
        # REAL-WORLD: PDF processing (e.g., using pdf2image) is required here.
        return True # Assume valid for now if it's a PDF

    # 2. Image Validation and SIMULATED Stamp Check
    try:
        # Check if the filename contains 'stamp' for easy testing
        if "stamp" in os.path.basename(file_path).lower():
            # In a real scenario, the CV logic would go here:
            # result = run_opencv_stamp_check(file_path)
            # return result
            print(f"DEBUG: Found 'stamp' in filename: {os.path.basename(file_path)} - SIMULATING VALID")
            return True # SIMULATE: Valid Stamp

        # Attempt to open and close the image to check for basic corruption
        img = Image.open(file_path)
        img.verify() # Verify file integrity
        
        # If no stamp keyword is found, and the file is valid, simulate a NO STAMP result
        print(f"DEBUG: Valid image, but no 'stamp' keyword. SIMULATING FAKE.")
        return False # SIMULATE: No Stamp (or real CV detection failed)

    except FileNotFoundError:
        print(f"ERROR: File not found at path: {file_path}")
        return "error"
    except Exception as e:
        # Catches file corruption, invalid image format errors, etc.
        print(f"VALIDATION ERROR for {file_path}: {e}")
        return "error"