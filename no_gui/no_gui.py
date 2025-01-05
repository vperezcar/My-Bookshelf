from api.search import SearchType, search_books
from model.user import UserBookStatus, UserBook
from utils.globals import DATABASE_CONNECTION, USER
import utils.constants.constants as constants
from utils.export import export_to_excel


def print_menu():
    for i, option in enumerate(constants.MAIN_OPTIONS):
        print(f"{i + 1}. {option}")


def print_books(books):
    for i, book in enumerate(books):
        print(f"{i}. {book.title} - {book.authors}")


# My books functions


def display_user_book(user_book):
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[0]} {user_book.status.name}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[1]} {user_book.score}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[2]} {user_book.book.title}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[3]} {user_book.book.authors}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[4]} {user_book.book.publisher}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[5]} {user_book.book.published_date}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[6]} {user_book.book.description}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[7]} {user_book.book.page_count}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[8]} {user_book.book.categories}")
    print(f"{constants.DISPLAY_USER_BOOK_ARRAY[9]} {user_book.book.language}")
    option = input(constants.WISH_TO_CHANGE_STATUS)
    if option.lower() == "s":
        global USER
        if user_book.status == UserBookStatus.READ:
            option = input(constants.READING_OR_WANT_TO_READ)
            USER.read_books.remove(user_book)
            if option.lower() == "l" or option.lower() == "r":
                user_book.status = UserBookStatus.READING
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.READING.value
                )
                USER.reading_books.append(user_book)
            else:
                user_book.status = UserBookStatus.WANT_TO_READ
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.WANT_TO_READ.value
                )
                USER.want_to_read_books.append(user_book)
        elif user_book.status == UserBookStatus.READING:
            option = input(constants.READ_OR_WANT_TO_READ)
            USER.reading_books.remove(user_book)
            if option.lower() == "r":
                user_book.status = UserBookStatus.READ
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.READ.value
                )
                USER.read_books.append(user_book)
            else:
                user_book.status = UserBookStatus.WANT_TO_READ
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.WANT_TO_READ.value
                )
                USER.want_to_read_books.append(user_book)
        else:
            option = input(constants.READ_OR_READING)
            USER.want_to_read_books.remove(user_book)
            if option.lower() == "r":
                user_book.status = UserBookStatus.READ
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.READ.value
                )
                USER.read_books.append(user_book)
            else:
                user_book.status = UserBookStatus.READING
                DATABASE_CONNECTION.update_user_book_status(
                    user_book.user_book_id, UserBookStatus.READING.value
                )
                USER.reading_books.append(user_book)


def print_user_books(user_books):
    for i, user_book in enumerate(user_books):
        print(f"{i}. {user_book.book.title} - {user_book.book.authors}")


def my_books():
    if USER.has_books():
        if USER.read_books:
            print(constants.MY_BOOKS_ARRAY[0])
            print_user_books(USER.read_books)
            selected_book = input(constants.SELECT_ONE_BOOK_TO_SEE_DETAILS)
            if selected_book:
                display_user_book(USER.read_books[int(selected_book)])
        if USER.reading_books:
            print(constants.MY_BOOKS_ARRAY[1])
            print_user_books(USER.reading_books)
            selected_book = input(constants.SELECT_ONE_BOOK_TO_SEE_DETAILS)
            if selected_book:
                display_user_book(USER.reading_books[int(selected_book)])
        if USER.want_to_read_books:
            print(constants.MY_BOOKS_ARRAY[2])
            print_user_books(USER.want_to_read_books)
            selected_book = input(constants.SELECT_ONE_BOOK_TO_SEE_DETAILS)
            if selected_book:
                display_user_book(USER.want_to_read_books[int(selected_book)])
    else:
        print(constants.NO_BOOKS)


# Search functions


def print_search_menu():
    print(f"1. {constants.SIMPLE_SEARCH}")
    print(f"2. {constants.ADVANCED_SEARCH}")
    print(f"3. {constants.EXIT}")


def print_simple_search():
    for i, search_type in enumerate(constants.SEARCH_TYPES):
        print(f"{i + 1}. {search_type}")


def display_book(book):
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[0]} {book.title}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[1]} {book.authors}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[2]} {book.published_date}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[3]} {book.description}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[4]} {book.page_count}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[5]} {book.publisher}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[6]} {book.categories}")
    print(f"{constants.DISPLAY_BOOK_NO_GUI_ARRAY[7]} {book.language}")
    option = input(constants.WISH_TO_ADD_TO_YOUR_BOOKS)
    if option.lower() == "s":
        global USER
        # Add book to the database if not exist
        book_id = DATABASE_CONNECTION.get_book_id(book.id)
        if not book_id:
            book_id = DATABASE_CONNECTION.add_book(book)
        # Add book to list
        user_book_id = DATABASE_CONNECTION.add_book_to_user(USER.user_id, book_id)
        USER.add_want_to_read_book(UserBook(user_book_id, USER.user_id, book_id, book))


def iterate_books(search, advanced_search=False, search_by_field=False, search_type=0):
    books = search_books(search, advanced_search, search_by_field, search_type)
    print(f"{constants.FOUND} {books.number_of_books} {constants.BOOKS}")
    number_of_books = books.number_of_books
    number_of_books_displayed = 0
    while True:
        print_books(books.books)
        number_of_books_displayed += len(books.books)
        selected_book = input(constants.SELECT_ONE_BOOK_TO_SEE_DETAILS)
        if selected_book:
            display_book(books.books[int(selected_book)])
        if number_of_books_displayed < number_of_books:
            option = input(constants.WISH_TO_SEE_MORE)
            if option.lower() != "s":
                break
            books = search_books(
                search,
                advanced_search,
                search_by_field,
                search_type,
                number_of_books_displayed,
            )
        else:
            break


def simple_search():
    search_by_field = False
    search = input(constants.ADD_SEARCH_TERM)
    print(constants.SELECT_FIELD)
    print_simple_search()
    search_type = int(input(constants.OPTION))
    if search_type > 0:
        search_by_field = True
        search_type -= 1
        if search_type > 6:
            search_type = 0
        print(f"{constants.LOOKING_FOR} {SearchType(search_type).name}")
    iterate_books(search, search_by_field=search_by_field, search_type=search_type)


def advanced_search():
    search_inputs = []
    search_inputs.append(input(constants.ADVANCED_SEARCH_INPUT))
    print(constants.ADVANCED_SEARCH_SPECIFIC_INPUT)
    search_fields = SearchType.__members__.keys()
    for field in search_fields:
        search_inputs.append(input(f"{field}: "))
    iterate_books(search_inputs, advanced_search=True)


def search():
    print_search_menu()
    option = input(constants.OPTION)
    if option == "1":
        simple_search()
    elif option == "2":
        advanced_search()
    else:
        print(constants.UNKNOWN_OPTION)


def export():
    fileName = input(constants.EXPORT_TO_EXCEL_INPUT)
    if not fileName.endswith(".xlsx"):
        fileName += ".xlsx"
    export_to_excel(fileName)
    print(constants.SUCCESS_EXPORT)


def no_gui_app():
    print(constants.WELCOME_MESSAGE)
    while True:
        print_menu()
        option = input(constants.OPTION)
        if option == "1":
            my_books()
        elif option == "2":
            search()
        elif option == "3":
            export()
        else:
            break
