from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import shutil, os

def main_home_screen():
    global main_screen

    global company_code
    global doc_type

    main_screen = Tk()
    main_screen.geometry('410x200')
    main_screen.title('Internal Tool')

    def destroy_window():
        # check if processing, prevent close
        # if not:
        main_screen.destroy()

    main_screen.protocol('WM_DELETE_WINDOW', destroy_window)  

    # Bring window to top
    main_screen.lift()
    main_screen.attributes('-topmost',True)
    main_screen.after_idle(main_screen.attributes,'-topmost',False)

    company_code = StringVar()
    doc_type = StringVar()

    company_label = Label(main_screen, text='Company Code:').place(x=80, y=40)
    Entry(main_screen, textvariable=company_code).place(x=180, y=40)

    doc_label = Label(main_screen, text='Document Type:').place(x=80, y=70)
    Entry(main_screen, textvariable=doc_type).place(x=180, y=70)

    Button(main_screen, text='Open Folder', command=folder_screen).place(x=140, y=100, height=30, width=100)

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
    global ccode
    global dtype
    global employee_id
    global lbox2
    global browse_screen

    ccode = company_code.get()
    dtype = doc_type.get()

    browse_screen = Tk()
    browse_screen.geometry('800x650')
    browse_screen.title('Internal Tool')

    employee_id = StringVar()

    Label(browse_screen, text='Company Code: ' + str(ccode)).place(x=20, y=10)
    Label(browse_screen, text='Document Type: ' + str(dtype)).place(x=200, y=10)
    Label(browse_screen, text='Files').place(x=80, y=70)
    Label(browse_screen, text='Employee ID').place(x=200, y=70)
    Label(browse_screen, text='Preview').place(x=510, y=55)

    flist = os.listdir(folder_selected)
    lbox = Listbox(browse_screen)
    lbox.place(x=20, y=95, width=150, height=500)
    lbox2 = Listbox(browse_screen)
    lbox2.place(x=170, y=95, width=150, height=500)

    def OnVsb(*args):
        lbox.yview(*args)
        lbox2.yview(*args)

    scrollbar = Scrollbar(lbox2, orient="vertical", command=OnVsb)
    scrollbar.pack(side="right", fill="y")
    lbox2.config(yscrollcommand=scrollbar.set)

    id_label = Label(browse_screen, text='Employee ID: ').place(x=20, y=40)
    employee_id1 = Entry(browse_screen, textvariable=employee_id)
    employee_id1.place(x=100, y=40, height=25, width=150)

    for item in flist:
        if item.startswith('.'): #Ignore Hidden Files
            continue
        lbox.insert(END, item)
        lbox2.insert(END, '')

    def opensystem(event):
        global file_id
        global selected
        file_id = StringVar()
        selected = lbox.curselection()[0]

        file1 = lbox.get(selected)
        file_id = file1
        file = fselected + "/" + file1

        Button(browse_screen, text='Save', command=id_files).place(x=260, y=40, height=25, width=50)

        img = Image.open(file)
        maxsize = (380, 500)
        im = img.resize(maxsize)
        img = ImageTk.PhotoImage(im)
        imglabel = Label(browse_screen, image=img)
        imglabel.image = img
        imglabel.pack()
        imglabel.place(x=350, y=80, width=380, height=500)

        # Bring window to top
        browse_screen.lift()
        browse_screen.attributes('-topmost', True)
        browse_screen.after_idle(browse_screen.attributes, '-topmost', False)
        browse_screen.focus_force()
        employee_id.set("")
        employee_id1.focus_set()
        
    def OnEntryDown(event):
        selected = lbox.curselection()[0]
        if selected < lbox.size()-1:
            lbox.select_clear(selected)
            selected += 1
            lbox.select_set(selected)
            lbox.event_generate("<<ListboxSelect>>")
        opensystem(event)

    def OnEntryUp(event):
        selected = lbox.curselection()[0]
        if selected > 0:
            lbox.select_clear(selected)
            selected -= 1
            lbox.select_set(selected)
            lbox.event_generate("<<ListboxSelect>>")
        opensystem(event)

    def id_files(event):
        selected = lbox.curselection()[0]
        empid = employee_id.get()
        lbox2.delete(selected)
        lbox2.insert(selected, empid)
        lbox.select_clear(selected)
        selected +=1
        employee_id.set("")
        lbox.select_set(selected)
        lbox.event_generate("<<ListboxSelect>>")

    lbox.bind("<<ListboxSelect>>", opensystem)
    browse_screen.bind("<Up>", OnEntryUp)
    browse_screen.bind("<Down>", OnEntryDown)
    employee_id1.bind('<Return>', id_files)
    selection = lbox.curselection()
    if not selection: # Default select first item in listbox
        lbox.select_set(0)
        lbox.event_generate("<<ListboxSelect>>")
        

    Button(browse_screen, text='Process', command=process_screen).place(x=400, y=600, height=30, width=300)

    browse_screen.mainloop()

def process_screen():
    global new_path

    new_path = StringVar()
    n = 0

    #create a new folder with document type as folder name
    new_path = os.mkdir(fselected + "/" + dtype)
    new_path1 = str(fselected + "/" + dtype)
    #list all files in selected folder
    # TODO Better to send a list of files instead of reading all files again to make sure we only process the files we have edited
    # i.e flist can be just a list and every input of employee id, we just do flist1.append(file_path)
    flist1 = os.listdir(fselected)
    #list all entries for employee id
    employeeid = list(lbox2.get(0, END))
    #get total count of files in selected folder
    count = len(flist1)

    for file in flist1:
        if file.startswith('.'): #Ignore Hidden Files
            continue
        fsrce = fselected + "/" + file
        #process only files
        if os.path.isfile(fsrce):
            emp_id = employeeid[n]
            if emp_id != "":
                #emp_id = employeeid[n]
                fname, file_ext = os.path.splitext(file)
                #rename files to copy
                dest_name = ccode + "_" + emp_id + "_" + dtype + file_ext
                fdest = new_path1  + "/" + dest_name
                shutil.copy(fsrce, fdest)

                #name of file to pdf
                dest_name_pdf = ccode + "_" + emp_id + "_" + dtype + ".pdf"
                fdest_pdf = new_path1  + "/" + dest_name_pdf
                #convert file to pdf
                im=Image.open(fdest)
                if im.mode == "RGBA":
                    im = im.convert("RGB")
                if not os.path.exists(fdest_pdf):
                    im.save(fdest_pdf, "PDF", resolution=100.0)
                #delete file in the folder
                os.remove(fdest)

            if n < count:
                n+=1

    process_complete()

def process_complete():
    global complete_screen

    complete_screen = Tk()
    complete_screen.geometry('200x100')
    complete_screen.title('Process Complete')

    Label(complete_screen, text='Processing Complete!').place(x=30, y=20)
    Button(complete_screen, text='OK!', command=destroy_screen).place(x=60, y=60, height=30, width=60)

def destroy_screen():
    browse_screen.destroy()
    complete_screen.destroy()

main_home_screen()
