import sqlite3
import json
from model.user import User, UserBook, UserBookStatus
from model.book import Book


class SQLite3Connection:
    conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self):
        self.conn = sqlite3.connect("db/books.db")
        self.cur = self.conn.cursor()
        # Create tables if not exists
        self.create_tables()

    def create_tables(self):
        self.create_book_table()
        self.create_user_table()
        self.create_user_books_table()

    def create_book_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT,
                title TEXT,
                authors TEXT,
                publisher TEXT,
                published_date TEXT,
                description TEXT,
                page_count INTEGER,
                categories TEXT,
                image_links TEXT,
                language TEXT
            )
            """
        )
        self.conn.commit()

    def create_user_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT
            )
            """
        )
        self.conn.commit()

    def create_user_books_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_books (
                user_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                score INTEGER DEFAULT 0,
                status INTEGER DEFAULT 2,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
            """
        )
        self.conn.commit()

    def add_user(self, username):
        self.cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
        self.conn.commit()

    def get_user(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        db_user = self.cur.fetchone()
        return User(db_user[0], db_user[1]) if db_user else None

    def add_book(self, book):
        self.cur.execute(
            """
            INSERT INTO books (
                id,
                title,
                authors,
                publisher,
                published_date,
                description,
                page_count,
                categories,
                image_links,
                language
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                book.id,
                book.title,
                json.dumps(book.authors),
                book.publisher,
                book.published_date,
                book.description,
                book.page_count,
                json.dumps(book.categories),
                json.dumps(book.image_links),
                book.language,
            ),
        )
        self.conn.commit()

        return self.cur.lastrowid

    def get_book_id(self, id):
        self.cur.execute("SELECT * FROM books WHERE id = ?", (id,))
        book = self.cur.fetchone()
        return None if book == None else book[0]

    def get_book(self, book_id):
        self.cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        db_book = self.cur.fetchone()
        return (
            Book(
                db_book[1],
                db_book[2],
                json.loads(db_book[3]),
                db_book[4],
                db_book[5],
                db_book[6],
                db_book[7],
                json.loads(db_book[8]),
                json.loads(db_book[9]),
                db_book[10],
            )
            if db_book
            else None
        )

    def get_books_by_user(self, user_id):
        self.cur.execute(
            """
            SELECT * FROM books
            JOIN user_books ON books.book_id = user_books.book_id
            WHERE user_books.user_id = ?
            """,
            (user_id,),
        )
        db_user_books = self.cur.fetchall()
        if db_user_books and len(db_user_books) > 0:
            user_books = []
            for db_user_book in db_user_books:
                book = Book(
                    db_user_book[1],
                    db_user_book[2],
                    json.loads(db_user_book[3]),
                    db_user_book[4],
                    db_user_book[5],
                    db_user_book[6],
                    db_user_book[7],
                    json.loads(db_user_book[8]),
                    json.loads(db_user_book[9]),
                    db_user_book[10],
                )
                book.book_id = db_user_book[0]
                user_book = UserBook(
                    db_user_book[11],
                    db_user_book[12],
                    db_user_book[13],
                    book,
                    db_user_book[14],
                    UserBookStatus(db_user_book[15]),
                )
                user_books.append(user_book)
            return user_books

    def add_book_to_user(self, user_id, book_id, status=2):
        self.cur.execute(
            "INSERT INTO user_books (user_id, book_id, status) VALUES (?, ?, ?)",
            (user_id, book_id, status),
        )
        self.conn.commit()

        return self.cur.lastrowid
    
    def update_user_book_status(self, user_book_id, status):
        self.cur.execute(
            "UPDATE user_books SET status = ? WHERE user_book_id = ?",
            (status, user_book_id),
        )
        self.conn.commit()

    def update_user_book_score(self, user_book_id, score):
        self.cur.execute(
            "UPDATE user_books SET score = ? WHERE user_book_id = ?",
            (score, user_book_id),
        )
        self.conn.commit()