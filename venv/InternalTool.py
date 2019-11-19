import shutil, os
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from scrollimage import ScrollableImage

def main_home_screen():
    global main_screen

    global company_code
    global doc_type

    main_screen = Tk()
    main_screen.geometry('420x240')
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
    global ccode
    global dtype
    global employee_id
    global lbox2
    global browse_screen
    global selected
    global process_dict

    process_dict = {}

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

    def numbers_only(x):
        value = ''.join(c for c in x if c.isdigit())
        if not value:
            return 0
        return int(value)

    flist = sorted(flist, key=numbers_only)  
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
    employee_id_input = Entry(browse_screen, textvariable=employee_id)
    employee_id_input.place(x=650, y=20, height=25, width=180)

    for item in flist:
        if item.startswith('.'): #Ignore Hidden Files
            continue
        if not os.path.isfile(folder_selected + '/' + item):
            continue
        lbox.insert(END, item)
        lbox2.insert(END, '-')
    
    selected = 0
    lbox.select_set(selected)

    # Delete na this if di na gagamitin
    # or ilipat mo ung pagpreview ng image dito :)
    # para mas madali basahin ung code
    #
    # def showcontent(event):
    #     x = lbox.curselection()[0]
    #     file1 = lbox.get(x)
    #     file = fselected + "/" + file1
    #     with open(file, 'rb') as file:
    #         file = file.read()


    def opensystem(event):
        global file_id
        global x
        file_id = StringVar()

        selection = lbox.curselection()
        if not selection: # Default select first item in listbox
            lbox.select_set(0)
            lbox.event_generate("<<ListboxSelect>>")
        x = lbox.curselection()[0]
        file1 = lbox.get(x)
        file_id = file1
        file = fselected + "/" + file1

        Button(browse_screen, text='Save', command=id_files).place(x=840, y=20, height=25, width=50)
        # Move this to show content method for better code readability
        img = ImageTk.PhotoImage(file=file)
        # maxsize = (380, 500)
        # im = img.resize(maxsize)
        show_image = ScrollableImage(browse_screen, image=img)
        # imglabel = Label(browse_screen, image=img)
        # imglabel.image = img
        show_image.pack()
        show_image.place(x=550, y=80, width=380, height=500)
    
    def OnEntryDown(event):
        selected = lbox.curselection()[0]
        if selected < lbox.size()-1:
            lbox.select_clear(selected)
            selected += 1
            lbox.select_set(selected)
        opensystem(event)

    def OnEntryUp(event):
        selected = lbox.curselection()[0]
        if selected > 0:
            lbox.select_clear(selected)
            selected -= 1
            lbox.select_set(selected)
        opensystem(event)
        

    def id_files(event=None):
        empid = employee_id.get()
        lbox2.delete(x)
        lbox2.insert(x, empid)
        process_dict[lbox.get(x)] = empid

    lbox.bind("<<ListboxSelect>>", opensystem)
    browse_screen.bind("<Down>", OnEntryDown)
    browse_screen.bind("<Up>", OnEntryUp)
    employee_id_input.bind('<Return>', id_files)
    # Redundant with LISTBOXSELECT + showcontent no longer used, replace with opensystem
    #lbox.bind("<Double-Button-1>", opensystem)

    Button(browse_screen, text='Process', command=process_screen).place(x=600, y=600, height=30, width=300)

    browse_screen.mainloop()

def process_screen():
    global new_path

    new_path = StringVar()
    n = 0

    # Check if current path is existing
    # if yes prompt user if delete or change folder

    #create a new folder with document type as folder name
    new_path = os.mkdir(fselected + "/" + dtype)
    new_path1 = str(fselected + "/" + dtype)
    #list all files in selected folder
    # TODO Better to send a list of files instead of reading all files again to make sure we only process the files we have edited
    # i.e flist can be just a list and every input of employee id, we just do flist1.append(file_path)
    flist1 = os.listdir(fselected)
    def numbers_only(x):
        value = ''.join(c for c in x if c.isdigit())
        if not value:
            return 0
        return int(value)

    flist1 = sorted(flist1, key=numbers_only) 
    #list all entries for employee id
    employeeid = list(lbox2.get(0, END))
    #get total count of files in selected folder
    count = len(flist1)

    for file, empid in list(process_dict.items()):
        print(f'Processing {file}')
        if file.startswith('.'): #Ignore Hidden Files
            continue
        if empid == '-':  # Ignore Files without Tag
            if n < count:
                n += 1 
            continue
        fsrce = fselected + "/" + file
        print(f'Source: {fsrce}')
        #process only files
        if os.path.isfile(fsrce):
            fname, file_ext = os.path.splitext(file)
            #rename files to copy
            dest_name = ccode + "_" + empid + "_" + dtype + file_ext
            fdest = new_path1  + "/" + dest_name
            shutil.copy(fsrce, fdest)

            #name of file to pdf
            dest_name_pdf = ccode + "_" + empid + "_" + dtype + ".pdf"
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
