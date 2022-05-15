# --------------- IMPORTS --------------- #
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import itertools
import pyperclip
from os import path

# --------------- Global Variables --------------- #
LABEL_FONT = "Ariel"
CUSTOM_WORDLIST = []
BACKGROUND_COLOR = "lavender"


# --------------- Make Dictionary --------------- #

# Checks if the file exist and creates it if it doesn't.
def does_file_exist():
    dic_name = name_input.get()
    if path.exists(dic_name):
        m_box = messagebox.askyesnocancel(
            "Overwrite file",
            f'A file with the name \n"{dic_name}" already exist.\n\nDo you want to overwrite it?',
        )

        if m_box:
            create_dic()
        else:
            messagebox.showinfo(title="Stopped!", message="Please change the name \nand try again.")
    else:
        create_dic()

# Creates the dictionary file based off the provided inputs
def create_dic():
    global CUSTOM_WORDLIST
    custom_wordlist = CUSTOM_WORDLIST
    dic_name = name_input.get()
    word_length = int(length_input.get())
    custom_chars = char_input.get()

    for char in custom_chars:
        custom_wordlist.append(char)
    with open(dic_name, "w") as dic_file:
        for passlength in [word_length]:
            combinations = itertools.product(custom_wordlist, repeat=passlength)
            for combination in combinations:
                dic_file.write(''.join(combination) + "\n")
        canvas.itemconfig(dic_title, text="Wordlist Created", fill="green")
        name_input.delete(0, 'end')
        char_input.delete(0, 'end')
        wl_file_input.insert(0, dic_name)


# --------------- Brute Force --------------- #

# Opens PDF file
def open_pdf():
    file = filedialog.askopenfilename()
    pdf_input.insert(0, file)

# Opens wordlist file
def open_wordlist():
    file = filedialog.askopenfilename()
    wl_file_input.insert(0, file)

# Starts attacking pdf file with the wordlist provided.
def pdf_bruteforce():
    start_brute_button.config(text="Running Bruteforce!")
    canvas.itemconfig(cracked_text, text="Running", fill="dodger blue")
    dic_name = wl_file_input.get()
    pdf_file = pdf_input.get()
    canvas.update()
    cracked = False

    # Loading passwords
    try:
        with open(dic_name) as f:
            lines = f.readlines()
    except FileNotFoundError:
        messagebox.showinfo(title="File not found", message="Dictionary file not found!")

    # Opening file
    print(f'Started cracking file "{pdf_file}" with dictionary "{dic_name}"')
    cracked_pass.delete(0, 'end')
    with open(pdf_file, 'rb') as input_file:
        reader = PdfFileReader(input_file)
        for password in lines:
            password = password.replace('\n', '')
            try:
                status = reader.decrypt(password)
                if status == 1:
                    cracked = True
                    break
            except:
                pass
    # Alerts the user of the status of the attack
    if cracked:
        canvas.itemconfig(cracked_text, text="Cracked!", fill="green")
        cracked_pass.insert(0, password)
        read_wl_name_input.insert(0, dic_name)
        read_pdf_input.insert(0, pdf_file)
        read_pass_input.insert(0, password)
    else:
        canvas.itemconfig(cracked_text, text="Failed!", fill="red")
    start_brute_button.config(text="Start Bruteforcing")

# Copies the cracked password to clipboard
def copy_button():
    password = cracked_pass.get()
    pyperclip.copy(password)


# --------------- Read Contents --------------- #

# Gives the user a choice to save or read the pdf
def read_or_save():
    switch = read_save_dropdown.get()
    pdf_f = read_pdf_input.get()
    save_f = save_to_file_input.get()
    cracked_p = read_pass_input.get()
    canvas.update()
    if switch == "Save":
        start_read_button.config(text=f"{switch}ing file!")

        with open(pdf_f, 'rb') as input_file, open(save_f, 'wb') as output_file:
            reader = PdfFileReader(input_file)
            reader.decrypt(cracked_p)
            writer = PdfFileWriter()

            for i in range(reader.getNumPages()):
                writer.addPage(reader.getPage(i))
            writer.write(output_file)
    else:
        start_read_button.config(text=f"{switch}ing pdf. Check Terminal!")

        with open(pdf_f, 'rb') as input_file:
            reader = PdfFileReader(input_file)
            reader.decrypt(cracked_p)
            for i in range(reader.getNumPages()):
                page = reader.getPage(i)
                page_content = page.extractText()
                print(f"-----------------------------------\nOUTPUT:\n\n{page_content}"
                      f"\n-----------------------------------")


# Save


# --------------- GUI --------------- #

# Tkinter GUI Settings
window = Tk()
window.title("Monk3y PDF Cracker")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Canvas
canvas = Canvas(width=800, height=700, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.pack()
gui_title = canvas.create_text(400, 20, text="PDF Bruteforcer", anchor='center', font=(LABEL_FONT, 30, "bold"))

# Lines
canvas.create_line(0, 60, 800, 60, width=4)
canvas.create_line(2, 60, 2, 700, width=4)
canvas.create_line(0, 380, 800, 380, width=1, dash=(4, 4))
canvas.create_line(400, 60, 400, 380, width=1, dash=(4, 4))
canvas.create_line(798, 60, 798, 700, width=4)
canvas.create_line(0, 698, 800, 698, width=4)

# Make Dictionary
dic_title = canvas.create_text(80, 120, text="Create Wordlist", anchor='w', font=(LABEL_FONT, 20, "bold"))

wordlist_name = canvas.create_text(80, 200, text="Name:", anchor='w', font=(LABEL_FONT, 14, "normal"))
name_input = Entry()
wl_name = canvas.create_window(270, 200, width=120, window=name_input)

wordlist_length = canvas.create_text(80, 230, text="Length:", anchor='w', font=(LABEL_FONT, 14, "normal"))
length_input = Entry()
wl_length = canvas.create_window(270, 230, width=120, window=length_input)

wordlist_char = canvas.create_text(80, 260, text="Characters:", anchor='w', font=(LABEL_FONT, 14, "normal"))
char_input = Entry()
wl_char = canvas.create_window(270, 260, width=120, window=char_input)

make_dic_button = Button(text="Create Wordlist", highlightthickness=0, command=does_file_exist)
canvas.create_window(200, 300, width=260, anchor='center', window=make_dic_button)

# Bruteforce
brute_title = canvas.create_text(480, 120, text="Bruteforce PDF", anchor='w', font=(LABEL_FONT, 20, "bold"))

wordlist_file_name = canvas.create_text(480, 200, text="Wordlist:", anchor='w', font=(LABEL_FONT, 14, "normal"))
wl_file_input = Entry()
wl_file_name = canvas.create_window(625, 200, width=120, window=wl_file_input)
wordlist_openfile_button = Button(text="Open", command=open_wordlist)
canvas.create_window(720, 200, width=60, anchor='center', window=wordlist_openfile_button)

pdf_file_name = canvas.create_text(480, 230, text="PDF:", anchor='w', font=(LABEL_FONT, 14, "normal"))
pdf_input = Entry()
pdf_name = canvas.create_window(625, 230, width=120, window=pdf_input)
pdf_openfile_button = Button(canvas, text="Open", command=open_pdf)
canvas.create_window(720, 230, width=60, anchor='center', window=pdf_openfile_button)

cracked_text = canvas.create_text(480, 260, text="Status", anchor='w', font=(LABEL_FONT, 14, "normal"))
cracked_pass = Entry()
canvas.create_window(625, 260, width=120, window=cracked_pass)
cracked_button = Button(canvas, text="Copy", command=copy_button)
canvas.create_window(720, 260, width=60, anchor='center', window=cracked_button)

start_brute_button = Button(text="Start Bruteforcing", highlightthickness=0, command=pdf_bruteforce)
canvas.create_window(610, 300, width=280, anchor='center', window=start_brute_button)

# Crack & Read
read_title = canvas.create_text(400, 410, text="Crack & Read/Save", anchor='center', font=(LABEL_FONT, 20, "bold"))

READ_OR_SAVE = [
    "Read",
    "Save"
]

read_save_dropdown = StringVar(canvas)
read_save_dropdown.set(READ_OR_SAVE[0])
dropdown = OptionMenu(canvas, read_save_dropdown, *READ_OR_SAVE)
dropdown_window = canvas.create_window(510, 450, width=220, window=dropdown)

read_wl_name = canvas.create_text(260, 500, text="Wordlist:", anchor='w', font=(LABEL_FONT, 14, "normal"))
read_wl_name_input = Entry()
read_wordlist_name = canvas.create_window(510, 500, width=220, window=read_wl_name_input)

read_pdf = canvas.create_text(260, 540, text="PDF:", anchor='w', font=(LABEL_FONT, 14, "normal"))
read_pdf_input = Entry()
read_pdf_name = canvas.create_window(510, 540, width=220, window=read_pdf_input)

read_pass = canvas.create_text(260, 580, text="Password:", anchor='w', font=(LABEL_FONT, 14, "normal"))
read_pass_input = Entry()
read_pass_name = canvas.create_window(510, 580, width=220, window=read_pass_input)

save_to_file = canvas.create_text(260, 620, text="Save As:", anchor='w', font=(LABEL_FONT, 14, "normal"))
save_to_file_input = Entry()
save_to_file_name = canvas.create_window(510, 620, width=220, window=save_to_file_input)

start_read_button = Button(text="Go Go Go!", highlightthickness=0, command=read_or_save)
canvas.create_window(440, 660, width=380, anchor='center', window=start_read_button)

window.mainloop()
