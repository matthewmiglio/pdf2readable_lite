import os

import fitz  # PyMuPDF
from PIL import Image
import io
import time
from tesseract import extract_text_from_image

DEFUALT_CHAR_LIMIT = 30000


def pdf_to_pil_images(pdf_path):
    pdf_path = pdf_path.replace("'",'').replace('"','')
    if ".pdf" not in pdf_path:
        print("Invalid file type")
        return

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    images = []

    # Iterate over each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)
        # Render page to an image (pixmap)
        pix = page.get_pixmap()
        # Convert pixmap to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)

    return images


def make_new_txt_file(pdf_path, lines, char_limit):
    def split_chars(chars, char_limit):
        group2lines = {}
        for i, char in enumerate(chars):
            index = i // char_limit
            if index not in group2lines:
                group2lines[index] = ""
            group2lines[index] += char

        return list(group2lines.values())

    line_groups = split_chars(lines, char_limit)
    for i, line_group in enumerate(line_groups):
        txt_path = pdf_path.replace(".pdf", f"_{i}.txt")
        with open(txt_path, "w") as f:
            f.write(line_group)


def pdf_to_text(pdf_path, char_limit):
    if ".pdf" not in pdf_path:
        return
    images = pdf_to_pil_images(pdf_path)
    lines = ""
    lines += f"Converting this pdf to text: {pdf_path}\n"
    lines += f"There are {len(images)} pages in this pdf\n\n\n"
    for i, image in enumerate(images):
        lines += f"Page {i+1}\n"
        lines += extract_text_from_image(image) + "\n"
        lines += "\n\n"
    make_new_txt_file(pdf_path, lines, char_limit)


def pdfs_to_text(pdf_folder_path, char_limit):
    files = os.listdir(pdf_folder_path)
    for file in files:
        print(f"\nConverting {file} to text")
        start_time = time.time()
        path = os.path.join(pdf_folder_path, file)
        pdf_to_text(path, char_limit)
        time_taken = str(time.time() - start_time).split(".")[0]
        print(f"Converted {file} to text in {time_taken} seconds")


def get_folder_path():
    s = "Enter a path containing PDFs: "
    while 1:
        path = input(s)
        if os.path.isdir(path):
            return path
        else:
            s = "Invalid path. Try again: "


def get_file_path():
    s = "Enter a path containing a PDF: "
    while 1:
        path = input(s)
        if ".pdf" in path:
            return path.replace('"','')
        else:
            s = "Invalid path. Try again: "


def get_input_type_input():
    s = "Select an input type:\n\t1) Folder\n\t2) File\n"
    while 1:
        inp = input(s)
        try:
            inp = int(inp)
            if inp in [1, 2]:
                if inp == 1:
                    return "Folder"
                else:
                    return "File"
        except:
            pass


def get_char_input():
    s = "Character limit: "
    while 1:
        inp = input(s)
        try:
            inp = int(inp)
            return inp
        except:
            pass

        if inp == "":
            return DEFUALT_CHAR_LIMIT


def main():
    print('\n'*50)
    print('')
    char_limit = get_char_input()
    input_type = get_input_type_input()
    if input_type == "Folder":
        fp = get_folder_path()
        pdfs_to_text(fp, char_limit)
    else:
        pdf_to_text(get_file_path(), char_limit)


if __name__ == "__main__":
    main()
