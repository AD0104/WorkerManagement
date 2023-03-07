from os import path
from shutil import copy2
from flask import current_app
from PyPDF2 import PdfReader, PdfWriter
def form_new_filename(args: list)->str:
    filename = ""
    separator, prefix = "_", "DOCUMENTO_QUINCENA.pdf"
    for arg in args:
        for section in arg.split(' '):
            filename = filename+section+separator
    filename += prefix
    return filename

def form_new_file(filename: str)->tuple:
    try:
        file_path = copy2(
            path.join(current_app.config["DOWNLOAD_FOLDER"], 'base.pdf'),
            path.join(current_app.config["DOWNLOAD_FOLDER"], filename)
        )
    except EnvironmentError as ee:
        print(ee)
        return ('',False)
    else:
        return (file_path, True)

def form_fill_file(user_data: dict, file_path: str):
    file_input = PdfReader(file_path)
    file_output = PdfWriter()

    page_to_fill = file_input.pages[0]

    page_fields = file_input.get_form_text_fields()
    print(page_fields)

    file_output.add_page(page_to_fill)

    pass
