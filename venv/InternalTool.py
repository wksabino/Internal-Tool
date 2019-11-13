from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
#import img2pdf
import os

def main_home_screen():
    global main_screen

    global company_code
    global doc_type

    main_screen = Tk()
    main_screen.geometry('270x180')
    main_screen.title('Internal Tool')

    company_code = StringVar()
    doc_type = StringVar()

    company_label = Label(main_screen, text='Company Code:').place(x=20, y=40)
    Entry(main_screen, textvariable=company_code).place(x=120, y=40)

    doc_label = Label(main_screen, text='Document Type:').place(x=20, y=70)
    Entry(main_screen, textvariable=doc_type).place(x=120, y=70)

    Button(main_screen, text='Open Folder', command=folder_screen).place(x=80, y=100, height=30, width=100)

    main_screen.mainloop()

def folder_screen():
    global folder_selected
    global fselected

    fselected = StringVar()

    folder = Tk()
    folder.withdraw()
    folder_selected = filedialog.askdirectory()
    fselected = folder_selected

    main_screen.destroy()
    browse_files()

def browse_files():
    global dtype
    global employee_id

    ccode = company_code.get()
    dtype = doc_type.get()

    browse_screen = Tk()
    browse_screen.geometry('1000x650')
    browse_screen.title('Internal Tool')

    employee_id = StringVar()

    Label(browse_screen, text='Company Code: ' + str(ccode)).place(x=20, y=20)
    Label(browse_screen, text='Document Type: ' + str(dtype)).place(x=280, y=20)
    Label(browse_screen, text='Files').place(x=120, y=55)
    Label(browse_screen, text='Employee ID').place(x=350, y=55)
    Label(browse_screen, text='Preview').place(x=710, y=55)

    flist = os.listdir(folder_selected)
    lbox = Listbox(browse_screen)
    lbox.place(x=20, y=80, width=220, height=500)
    lbox2 = Listbox(browse_screen)
    lbox2.place(x=280, y=80, width=220, height=500)

    scrollbar = Scrollbar(lbox, orient="vertical")
    scrollbar2 = Scrollbar(lbox2, orient="vertical")
    scrollbar.config(command=lbox.yview)
    scrollbar2.config(command=lbox2.yview)
    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side="right", fill="y")

    lbox.config(yscrollcommand=scrollbar.set)
    lbox2.config(yscrollcommand=scrollbar2.set)

    id_label = Label(browse_screen, text='Add Employee ID: ').place(x=550, y=20)
    Entry(browse_screen, textvariable=employee_id).place(x=650, y=20, height=25, width=180)

    for item in flist:
        lbox.insert(END, item)
        lbox2.insert(END, '<Add Employee ID>')

    def showcontent(event):
        x = lbox.curselection()[0]
        file1 = lbox.get(x)
        file = fselected + "/" + file1
        with open(file, 'rb') as file:
            file = file.read()

    def opensystem(event):
        global file_id
        global x
        file_id = StringVar()

        x = lbox.curselection()[0]
        file1 = lbox.get(x)
        file_id = file1
        file = fselected + "/" + file1

        Button(browse_screen, text='Save', command=id_files).place(x=840, y=20, height=25, width=50)

        img = Image.open(file)
        maxsize = (380, 500)
        im = img.resize(maxsize)
        img = ImageTk.PhotoImage(im)
        imglabel = Label(browse_screen, image=img).place(x=550, y=80, width=380, height=500)
        imglabel.pack(side="bottom", fill="both", expand="yes")

    def id_files():
        empid = employee_id.get()
        lbox2.delete(x)
        lbox2.insert(x, empid)

    lbox.bind("<<ListboxSelect>>", showcontent)
    lbox.bind("<Double-Button-1>", opensystem)

    Button(browse_screen, text='Process', command=process_screen).place(x=600, y=600, height=30, width=300)

    browse_screen.mainloop()

def process_screen():
    os.mkdir(fselected + "/" + dtype)
'''    
    flist1 = os.listdir(fselected)
    for item in flist1:
        pdffolder = fselected + "/" + dtype
        image = Image.open(fselected)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(pdffolder, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
'''
main_home_screen()
