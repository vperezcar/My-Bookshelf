import requests
from model.book import Book
from enum import Enum


class Search:
    books: list
    number_of_books: int

    def __init__(self, books, number_of_books):
        self.books = books
        self.number_of_books = number_of_books


class SearchType(Enum):
    Titulo = 0
    Autor = 1
    Editora = 2
    Categoria = 3
    ISBN = 4
    LCCN = 5
    OCLC = 6


ADVANCED_SEARCH_QUERIES = [
    "intitle:",
    "inauthor:",
    "inpublisher:",
    "subject:",
    "isbn:",
    "lccn:",
    "oclc:",
]


def search_books(
    search,
    advanced_search=False,
    search_by_field=False,
    search_type=0,
    start_index=0,
    max_results=10,
):
    if advanced_search:
        return advanced_search_books(search, start_index, max_results)
    return simple_search_books(
        search, search_by_field, search_type, start_index, max_results
    )


def simple_search_books(
    search, search_by_field=False, search_type=0, start_index=0, max_results=10
):
    if not search_by_field:
        search_query = f"https://www.googleapis.com/books/v1/volumes?q={search}&startIndex={start_index}&maxResults={max_results}"
    else:
        search_query = f"https://www.googleapis.com/books/v1/volumes?q={ADVANCED_SEARCH_QUERIES[search_type]}{search}&startIndex={start_index}&maxResults={max_results}"
    response = requests.get(search_query).json()

    books = []
    for book in response["items"]:
        books.append(parse_book(book))

    return Search(books, response["totalItems"])


def advanced_search_books(search_inputs, start_index=0, max_results=10):
    search_query = "https://www.googleapis.com/books/v1/volumes?q="
    if search_inputs[0]:
        search_query += f"{search_inputs[0]}"
    for search in search_inputs[1:]:
        if search:
            search_query += (
                f"+{ADVANCED_SEARCH_QUERIES[search_inputs.index(search) - 1]}{search}"
            )
    search_query += f"&startIndex={start_index}&maxResults={max_results}"
    response = requests.get(search_query).json()

    books = []
    for book in response["items"]:
        books.append(parse_book(book))

    return Search(books, response["totalItems"])


def parse_book(book):
    volume_info = book["volumeInfo"]
    return Book(
        id=book["id"],
        title=volume_info.get("title", None),
        authors=volume_info.get("authors", None),
        publisher=volume_info.get("publisher", None),
        published_date=volume_info.get("publishedDate", None),
        description=volume_info.get("description", "No description available"),
        page_count=volume_info.get("page_count", None),
        categories=volume_info.get("categories", None),
        image_links=volume_info.get("imageLinks", None),
        language=volume_info.get("language", None),
    )
