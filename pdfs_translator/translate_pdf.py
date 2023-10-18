from deep_translator import GoogleTranslator
from pdf_parser import parser, path_lighter
import os


def connect(file_name):
    following_text = open(file_name, "rb")
    return following_text


def get_amount_of_symbols(file_name):
    text = connect(file_name)
    result = len(text.read())
    text.close()
    return result


def translate(file, source, target):
    parser(file)
    symbols_amount = get_amount_of_symbols(file)
    path_to_folder = path_lighter(file[:-4])
    name_to_translate = path_to_folder + "_for_translate"
    following_text = connect(name_to_translate)

    translated_text = open(path_to_folder + '_translated_text', "w")

    while True:
        try:
            if symbols_amount < 0:
                translated_text.close()
                # remove(name_to_translate)
                break

            translated = GoogleTranslator(source=source, target=target).\
                translate(following_text.read(4999).decode('latin-1'))
            translated_text.write(translated)

            symbols_amount -= 4999

        except Exception as ex:
            print(ex)
            break

