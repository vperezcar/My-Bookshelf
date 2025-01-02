from tkinter import *
from searchform import SearchForm


class BookApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("My Book App")
        self.minsize(1280, 720)
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")

        frm = SearchForm(self)
        frm.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    BookApp().mainloop()
