from tkinter import filedialog
from tkinter import *

class LoginScreen:
    def __init__(self):
        self.master =  Tk()
        self.master.geometry('410x200')
        self.master.title('Login')
        self.master.lift()
        self.master.attributes('-topmost',True)
        self.master.after_idle(self.master.attributes,'-topmost',False)

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
        print(self.username.get())
        print(self.password.get())
        # Call login API here
        # If success open upload Screen and pass token
        self.master.destroy()
        # Else Display error

        
    