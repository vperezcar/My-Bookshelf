from tkinter import *
from tkinter.ttk import Combobox
from searchapi import search_books, SearchType
from searchresult import SearchResult


class SearchForm(Frame):
    search_type: int

    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.search_option = Combobox(
            self, values=[search_type.name for search_type in SearchType]
        )
        self.search_option.grid(row=0, column=0)
        self.search_option.current(0)
        self.search_type = 0
        self.search_option.bind(
            "<<ComboboxSelected>>", lambda event: self.combo_event()
        )

        self.search_entry = Entry(self)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind("<Return>", lambda event: self.search())

        self.search_button = Button(self, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2)

        # self.result_frame = Listbox(self)
        # self.result_frame = SearchResult(self)
        # self.result_frame.grid(row=1, columnspan=3, sticky="nsew")

    def search(self):
        search_input = self.search_entry.get()
        if search_input:
            result = search_books(search_input, self.search_type)
            for book in result.books:
                self.result_frame.add_book(book)
            self.search_entry.delete(0, END)

    def combo_event(self):
        self.search_type = self.search_option.current()
