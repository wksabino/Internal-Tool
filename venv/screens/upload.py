from tkinter import filedialog
from tkinter import *

from api.login import loginAPI
from api.upload_doc import uploadDocAPI


class UploadProgressScreen:
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.master = parent.master

        self.screen =  Tk()
        self.screen.geometry('410x600')
        self.screen.title('Progress')
        self.screen.lift()
        self.screen.attributes('-topmost',True)
        self.screen.after_idle(self.master.attributes,'-topmost',False)

        lbox = Listbox(self.screen)
        lbox.place(x=20, y=95, width=150, height=500)
        lbox2 = Listbox(self.screen)
        lbox2.place(x=170, y=95, width=150, height=500)

        self.start()

        self.screen.mainloop()
    
    def start(self):
        print(self.parent.data)
        print(self.parent.token)
        print(self.parent.doc_type)
        print(self.parent.company_code)
        # Iterate each file in data
        # success, message = uploadDocAPI(
        #     self.parent.token,
        #     #file here,
        #     #type here,
        #     #employee_id. here
        #     self.parent.company_code
        # )


class UploadScreen:
    def __init__(self, token, data_dict, company_code, doc_type):
        if not token:
            raise Exception('No Token passed')

        self.token = token
        self.data = data_dict
        self.company_code = company_code
        self.doc_type = doc_type
        self.master =  Tk()
        self.master.geometry('410x200')
        self.master.title('Upload Data')
        self.master.lift()
        self.master.attributes('-topmost',True)
        self.master.after_idle(self.master.attributes,'-topmost',False)
        
        if not self.data:
            label = Label(self.master, text='No Data for uploading').place(x=80, y=40)
        else:
            label = Label(self.master, text='Ready to upload {} items'.format(len(self.data.items()))).place(x=80, y=40)
            upload_button = Button(self.master, text='Start Upload', command=self.upload)
            upload_button.place(x=140, y=100, height=30, width=100)

        self.master.mainloop()

    def upload(self):
        UploadProgressScreen(self)

        
    