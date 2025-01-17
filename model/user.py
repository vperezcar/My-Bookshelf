from enum import Enum
from model.book import Book


class UserBookStatus(Enum):
    READ = 0
    READING = 1
    WANT_TO_READ = 2


class UserBook:
    user_book_id: int
    user_id: int
    book_id: int
    score: int
    status: UserBookStatus
    update_date: str
    book: Book

    def __init__(
        self,
        user_book_id,
        user_id,
        book_id,
        book,
        score=0,
        status=UserBookStatus.WANT_TO_READ,
        update_date=None,
    ):
        self.user_book_id = user_book_id
        self.user_id = user_id
        self.book_id = book_id
        self.book = book
        self.score = score
        self.status = status
        self.update_date = update_date


class User:
    user_id: int
    username: str
    want_to_read_books: list
    reading_books: list
    read_books: list

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.want_to_read_books = []
        self.reading_books = []
        self.read_books = []

    def add_want_to_read_book(self, user_book):
        self.want_to_read_books.append(user_book)

    def add_books(self, user_books):
        if user_books:
            for user_book in user_books:
                if user_book.status == UserBookStatus.READ:
                    self.read_books.append(user_book)
                elif user_book.status == UserBookStatus.READING:
                    self.reading_books.append(user_book)
                else:
                    self.want_to_read_books.append(user_book)

    def has_books(self):
        return bool(self.want_to_read_books or self.reading_books or self.read_books)

    def get_years_read_book(self):
        years = []
        for user_book in self.read_books:
            year = user_book.update_date.split("/")[2].split(" ")[0]
            if year not in years:
                years.append(year)
        return years

    def get_years_book(self):
        years = []
        for user_book in self.get_books():
            year = user_book.update_date.split("/")[2].split(" ")[0]
            if year not in years:
                years.append(year)
        return years

    def get_books(self):
        return self.read_books + self.reading_books + self.want_to_read_books
