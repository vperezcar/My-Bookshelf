import sqlite3_connection.sqlite3_connection as sqlite3_connection
from model.user import UserBook, UserBookStatus

# Database connection used to retrieve and store data
DATABASE_CONNECTION = None

# User logged in the application
USER = None

# Main options
MAIN_OPTIONS = ["Mis Libros", "Búsqueda", "Salir"]

# User book tabs
USER_BOOK_TABS = ["Leído", "Leyendo", "Quiero leer"]

# Search types
SEARCH_TYPES = ["Todo", "Título", "Autor", "Editorial", "Categoría", "ISBN", "LCCN", "OCLC"]

def initialize_database(user):
    global DATABASE_CONNECTION, USER
    DATABASE_CONNECTION = sqlite3_connection.SQLite3Connection()

    USER = DATABASE_CONNECTION.get_user(user)
    if not USER:
        DATABASE_CONNECTION.add_user(user)
        USER = DATABASE_CONNECTION.get_user(user)

    # Add books to the user from the database
    USER.add_books(DATABASE_CONNECTION.get_books_by_user(USER.user_id))

def update_user_book_status(user_book, status):
    old_status = user_book.status
    if old_status == UserBookStatus.READ:
        USER.read_books.remove(user_book)
    elif old_status == UserBookStatus.READING:
        USER.reading_books.remove(user_book)
    else:
        USER.want_to_read_books.remove(user_book)
    DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, status)
    if status == UserBookStatus.READ.value:
        USER.read_books.append(user_book)
    elif status == UserBookStatus.READING.value:
        USER.reading_books.append(user_book)
    else:
        USER.want_to_read_books.append(user_book)

def update_user_book_score(user_book, score):
    DATABASE_CONNECTION.update_user_book_score(user_book.user_book_id, score)

def update_user_book_update_date(user_book, update_date):
    DATABASE_CONNECTION.update_user_book_update_date(user_book.user_book_id, update_date)

def add_book_to_user(book, status):
    book_id = DATABASE_CONNECTION.get_book_id(book.id)
    if not book_id:
        book_id = DATABASE_CONNECTION.add_book(book)

    user_book_id = DATABASE_CONNECTION.add_book_to_user(USER.user_id, book_id, status)

    user_book = UserBook(user_book_id, USER.user_id, book_id, book, status=UserBookStatus(status))
    if status == UserBookStatus.READ.value:
        USER.read_books.append(user_book)
    elif status == UserBookStatus.READING.value:
        USER.reading_books.append(user_book)
    else:
        USER.want_to_read_books.append(user_book)

    return user_book

def remove_book_from_user(user_book):
    if user_book.status == UserBookStatus.READ:
        USER.read_books.remove(user_book)
    elif user_book.status == UserBookStatus.READING:
        USER.reading_books.remove(user_book)
    else:
        USER.want_to_read_books.remove(user_book)
    DATABASE_CONNECTION.remove_book_from_user(user_book.user_book_id)

def get_user_book_by_id(id):
    for user_book in USER.want_to_read_books + USER.reading_books + USER.read_books:
        if user_book.book.id == id:
            return user_book
    return None