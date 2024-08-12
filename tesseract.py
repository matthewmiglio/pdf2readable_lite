import pytesseract
import os


def get_tesseract_path():
    # get program files dir
    path = os.environ["ProgramFiles"]
    path = os.path.join(path, "Tesseract-OCR", "tesseract.exe")

    return path


pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()


def extract_text_from_image(img):
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", " ")
    return text
