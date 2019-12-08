from tkinter import *
from screens.initial import InitialScreen

from screens.login import LoginScreen

COMPANY_CODE = None
DOC_TYPE = None

def main_home_screen():
    global browse_screen
    # TODO Need to create Class for Browse Screen!
    browse_screen = Tk()
    browse_screen.geometry('800x650')
    browse_screen.title('Internal Tool')

    InitialScreen(browse_screen)


main_home_screen()
