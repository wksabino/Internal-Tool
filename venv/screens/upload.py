from tkinter import filedialog
from tkinter import *

from api.login import loginAPI
from api.upload_doc import uploadDocAPI


class UploadProgressScreen:
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.master = self.parent.master
        self.screen =  Tk()
        self.screen.geometry('410x600')
        self.screen.title('Progress')
        self.screen.lift()
        self.screen.attributes('-topmost',True)

        message = "Currently processing: "

        message_label = Label(self.screen, text=message).place(x=80, y=30)


        Label(self.screen, text='Success').place(x=80, y=70)
        Label(self.screen, text='Failed').place(x=200, y=70)

        self.success_box = Listbox(self.screen)
        self.success_box.place(x=20, y=95, width=150, height=500)
        self.fail_box = Listbox(self.screen)
        self.fail_box.place(x=170, y=95, width=150, height=500)

        self.start()

        self.screen.mainloop()
    
    def start(self):
        
        # Iterate each file in data
        for filename, employee_id in self.parent.data.items():
            #Get the file
            actual_file = open("{}/{}".format(self.parent.selected_folder, filename), 'rb')
            success, instance, message = uploadDocAPI(
                self.parent.token,
                actual_file,
                self.parent.doc_type,
                employee_id,
                self.parent.company_code
            )
            if success:
                self.success_box.insert(END, instance)
            else:
                self.fail_box.insert(END, "{}-{}".format(message, instance))


class UploadScreen:
    def __init__(self, token, data_dict, company_code, doc_type, selected_folder):
        if not token:
            raise Exception('No Token passed')

        self.token = token
        self.data = data_dict
        self.company_code = company_code
        self.doc_type = doc_type
        self.selected_folder = selected_folder
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

        
    