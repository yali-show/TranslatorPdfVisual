import config
import translate_pdf
import platform
from shutil import rmtree
from datetime import datetime
from functools import partial
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import *
from tkinter.ttk import *



window = Tk()
window.title("PDF translator")
window.geometry('600x350')

choices = config.languages

widgets = set()

tabs = Notebook(window, width=600, height=600)
tab_text = Frame(tabs)
tab_setup = Frame(tabs)
tab_files = Frame(tabs)

text_display = scrolledtext.ScrolledText(tab_text)
original_text = scrolledtext.ScrolledText(tab_text)
treeview = Treeview(tab_files, columns=("lastmod"))
treeview.tag_configure('odd', background='#eee')
treeview.tag_configure('even', background='#ddd')
treeview.heading("#0", text="File")
treeview.heading("lastmod", text="Saved")
treeview.grid(padx=10, pady=10, sticky=NSEW)


def open_file(path, i=None):

    translated_path = f'/Users/ilyabeliy/translated_files/{path}/{path}_translated_text'
    file = open(translated_path)
    file = file.read()
    text_display.delete('1.0', END)
    text_display.insert(INSERT, file)

    original_text_path = f'/Users/ilyabeliy/translated_files/{path}/{path}_for_translate'
    file = open(original_text_path)
    file = file.read()
    original_text.delete('1.0', END)
    original_text.insert(INSERT, file)


treeview.tag_bind('row', "<Button-2>", lambda event: popupmenu_command(event))

# TODO have to make communication of files in different folders and paths to "translated_files"
# TODO exe file to work with folderlders in it


def update_files():
    files = translate_pdf.os.listdir('/Users/ilyabeliy/translated_files')
    path_to_file = ...
    for file in files:
        if file not in widgets:
            treeview.tag_bind(file, '<Double-Button-1>', partial(open_file, file))

            if platform.system() == 'Windows':
                data = translate_pdf.os.path.getmtime(f'/Users/ilyabeliy/translated_files/{file}')
                data = datetime.fromtimestamp(data)

            else:
                stat = translate_pdf.os.stat(f'/Users/ilyabeliy/translated_files/{file}')
                data = datetime.fromtimestamp(stat.st_mtime)

            if files.index(file) % 2 == 0:
                treeview.insert(
                    "",
                    END,
                    text=file,
                    values=(data,), tags=(file, "row", 'even')
                )

            else:
                treeview.insert(
                    "",
                    END,
                    text=file,
                    values=(data,), tags=(file, "row", 'odd')
                )

            widgets.add(file)


def delete_files(file_name, row_id):
    treeview.delete(row_id)
    rmtree(f'/Users/ilyabeliy/translated_files/{file_name}')
    widgets.remove(file_name)


def popupmenu_command(event):
    row_id = treeview.identify_row(event.y)
    row_values = treeview.item(row_id)['text']
    popupmenu = Menu(treeview, tearoff=0)
    popupmenu.add_command(label='Open', accelerator='return', command=partial(open_file, row_values))
    popupmenu.add_command(label='Delete', accelerator='Delete', command=partial(delete_files, row_values, row_id))
    popupmenu.post(event.x_root, event.y_root)


update_files()

style = Style()
style.theme_use('default')

tabs.add(tab_setup, text='Translate')
tabs.add(tab_files, text='Files')
tabs.add(tab_text, text='Read text')


source_variable = StringVar(tab_setup)
target_variable = StringVar(tab_setup)


source = OptionMenu(tab_setup, source_variable, *choices)
target = OptionMenu(tab_setup, target_variable, *choices)
source_variable.set('- auto -')
target_variable.set('- choose option -')


path_variable = StringVar(tab_setup)
filepathlabel = Label(tab_setup, textvariable=path_variable, anchor="center")

can_run_file = False


def set_file_button():
    global can_run_file
    file_path = filedialog.askopenfilename()
    if file_path[-3:] == 'pdf':
        path_variable.set(file_path)
        can_run_file = True

    else:
        path_variable.set('Your file is not pdf type')
        can_run_file = False


def start_button_command():
    if can_run_file and target_variable.get() != '- choose option -':
        source_lang = choices[source_variable.get()]
        target_lang = choices[target_variable.get()]
        translate_pdf.translate(path_variable.get(), source=source_lang, target=target_lang)
        path = translate_pdf.path_lighter(path_variable.get()[:-4])
        original_text_path = path + '_for_translate'
        path = path + '_translated_text'
        text = open(path)
        text = text.read()
        text_display.delete(0.1, END)
        text_display.insert(INSERT, text)

        file = open(original_text_path)
        file = file.read()
        original_text.delete('1.0', END)
        original_text.insert(INSERT, file)
        update_files()

    else:
        messagebox.showerror(title='Something went wrong..',
                             message='Check your arguments')


start_button = Button(tab_setup, text='Get translation', command=start_button_command)
set_button = Button(tab_setup, text='Choose file', command=set_file_button)

label_image = Label(tab_setup, text='PDF translator', anchor=CENTER,
                    background='blue', foreground='white')


label_from = Label(tab_setup, text='Translate from', anchor="center")
label_to = Label(tab_setup, text='Translate to', anchor="center")
tabs.pack(padx=10, pady=10, expand=1, fill=BOTH)

source.config(width=15)
target.config(width=15)
set_button.config(width=15)
start_button.config(width=15)
filepathlabel.config(width=60)


text_display.pack(side='right', padx=10, expand=1, fill=BOTH)
original_text.pack(side='left', padx=10, expand=1, fill=BOTH)

label_image.grid(row=0, columnspan=3, column=0, padx=10, pady=10, sticky=NSEW)

label_from.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
source.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)
label_to.grid(row=1, column=2, padx=10, pady=10, sticky=NSEW)
target.grid(row=2, column=2, padx=10, pady=10, sticky=NSEW)
set_button.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)
start_button.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)
filepathlabel.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)
tab_setup.grid_columnconfigure(1, weight=1)
tab_setup.grid_columnconfigure(0, weight=1)
tab_setup.grid_columnconfigure(2, weight=1)
tab_setup.grid_rowconfigure(0, weight=1)

tab_files.grid_rowconfigure(0, weight=1)
tab_files.grid_columnconfigure(0, weight=1)


window.mainloop()
