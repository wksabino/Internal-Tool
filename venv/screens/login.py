from tkinter import filedialog
from tkinter import *

from api.login import loginAPI
from screens.upload import UploadScreen

class LoginScreen:
    def __init__(self, *args, **kwargs):
        self.master =  Tk()
        self.master.geometry('410x200')
        self.master.title('Login')
        self.master.lift()
        self.master.attributes('-topmost',True)
        self.master.after_idle(self.master.attributes,'-topmost',False)
        self.kwargs = kwargs
        username_label = Label(self.master, text='Username:').place(x=80, y=40)
        self.username = Entry(self.master)
        self.username.place(x=180, y=40)
        password_label = Label(self.master, text='Password:').place(x=80, y=70)
        self.password = Entry(self.master, show='*')
        self.password.place(x=180, y=70)

        login_button = Button(self.master, text='Login', command=self.login)
        login_button.place(x=140, y=100, height=30, width=100)
        self.master.mainloop()
    
    def login(self):
        # Call login API here
        success, message = loginAPI(self.username.get(), self.password.get())
        if success:
            token = message
            # Open Upload Screen and pass token
            print(self.kwargs)
            if 'action' in self.kwargs and self.kwargs['action'] == 'upload' and 'data' in self.kwargs:
                
                data_dict = self.kwargs['data']
                company_code = self.kwargs['company_code']
                doc_type = self.kwargs['doc_type']
                UploadScreen(token, data_dict, company_code, doc_type)
            self.master.destroy()
        else:
            error = Label(self.master, text="{}".format(message)).place(x=80, y=130)
    

        
    