import sqlite3_connection.sqlite3_connection as sqlite3_connection
from model.user import UserBookStatus

# Database connection used to retrieve and store data
DATABASE_CONNECTION = None

# User logged in the application
USER = None

# User book tabs
USER_BOOK_TABS = ["Leído", "Leyendo", "Quiero leer"]

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