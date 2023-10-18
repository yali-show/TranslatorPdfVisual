import sys
import os
import PyPDF2


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def path_lighter(path):
    vise_path = path.split('/')
    path = f'/Users/ilyabeliy/translated_files/{vise_path[-1]}'

    if not os.path.exists(path):
        os.mkdir(f'/Users/ilyabeliy/translated_files/{vise_path[-1]}')

    path_to_folder = f'/Users/ilyabeliy/translated_files/{vise_path[-1]}/{vise_path[-1]}'
    return path_to_folder


def writer(all_pages, pages_amount, name):
    with open(name + "_for_translate", "w") as for_translate:
        for page_number in range(pages_amount):
            page = all_pages.pages[page_number]
            for_translate.write(page.extract_text())


def parser(name):
    with open(name, 'rb') as file:
        file_reader = PyPDF2.PdfReader(file)
        page_amount = len(file_reader.pages)
        path = path_lighter(name[:-4])
        writer(file_reader, page_amount, path)
