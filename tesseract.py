import pytesseract
import os
from PIL import Image  # Ensure you have Pillow installed for image handling


def get_tesseract_path():
    # get program files dir
    path = os.environ["ProgramFiles"]
    path = os.path.join(path, "Tesseract-OCR", "tesseract.exe")
    return path


pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()


def extract_text_from_image(img_path):
    # Open the image file
    with Image.open(img_path) as img:
        # Use Tesseract to extract text, specify English language, and use appropriate page segmentation mode
        text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    text = text.replace("\n", " ")
    return text


if __name__ == "__main__":
    p = r"C:\Users\matt\Desktop\phil_readings\Singer_All Animals Are Equal.png"
    t = extract_text_from_image(p)
    print(t)
