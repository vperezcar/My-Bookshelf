from tkinter import *


class SearchResult(Frame):

    def __init__(self, parent):
        super().__init__(parent)

    def add_book(self, book):
        Label(self, text=f"{book.title} - {book.authors}").grid(sticky="ew")
