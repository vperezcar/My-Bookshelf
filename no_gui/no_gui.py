from api.search import SearchType, search_books
from model.user import UserBookStatus, UserBook
from utils.globals import DATABASE_CONNECTION, USER

def print_menu():
    print("1. Mis Libros")
    print("2. Busqueda")
    print("3. Salir")

def print_books(books):
    for i, book in enumerate(books):
        print(f"{i}. {book.title} - {book.authors}")

# My books functions

def display_user_book(user_book):
    print(f"Titulo: {user_book.book.title}")
    print(f"Autores: {user_book.book.authors}")
    print(f"Fecha de publicacion: {user_book.book.published_date}")
    print(f"Descripcion: {user_book.book.description}")
    print(f"Numero de paginas: {user_book.book.page_count}")
    print(f"Editora: {user_book.book.publisher}")
    print(f"Categorias: {user_book.book.categories}")
    print(f"Lenguaje: {user_book.book.language}")
    option = input(f"Quiere cambiar el estado de este libro? (s/n): ")
    if option.lower() == "s":
        global USER
        if user_book.status == UserBookStatus.READ:
            option = input(f"Leyendo (l) o Quiero leerlo (q): ")
            USER.read_books.remove(user_book)
            if option.lower() == "l":
                user_book.status = UserBookStatus.READING
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.READING.value)
                USER.reading_books.append(user_book)
            else:
                user_book.status = UserBookStatus.WANT_TO_READ
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.WANT_TO_READ.value)
                USER.want_to_read_books.append(user_book)
        elif user_book.status == UserBookStatus.READING:
            option = input(f"Leido (r) o Quiero leerlo (q): ")
            USER.reading_books.remove(user_book)
            if option.lower() == "r":
                user_book.status = UserBookStatus.READ
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.READ.value)
                USER.read_books.append(user_book)
            else:
                user_book.status = UserBookStatus.WANT_TO_READ
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.WANT_TO_READ.value)
                USER.want_to_read_books.append(user_book)
        else:
            option = input(f"Leido (r) o Leyendo (l): ")
            USER.want_to_read_books.remove(user_book)
            if option.lower() == "r":
                user_book.status = UserBookStatus.READ
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.READ.value)
                USER.read_books.append(user_book)
            else:
                user_book.status = UserBookStatus.READING
                DATABASE_CONNECTION.update_user_book_status(user_book.user_book_id, UserBookStatus.READING.value)
                USER.reading_books.append(user_book)

def print_user_books(user_books):
    for i, user_book in enumerate(user_books):
        print(f"{i}. {user_book.book.title} - {user_book.book.authors}")

def my_books():
    if USER.has_books():
        if USER.read_books:
            print("Libros leidos:")
            print_user_books(USER.read_books)
            selected_book = input(
                "Seleccione un libro para ver mas detalles (o presione enter para continuar): "
            )
            if selected_book:
                display_user_book(USER.read_books[int(selected_book)])
        if USER.reading_books:
            print("Libros en lectura:")
            print_user_books(USER.reading_books)
            selected_book = input(
                "Seleccione un libro para ver mas detalles (o presione enter para continuar): "
            )
            if selected_book:
                display_user_book(USER.reading_books[int(selected_book)])
        if USER.want_to_read_books:
            print("Libros que quiero leer:")
            print_user_books(USER.want_to_read_books)
            selected_book = input(
                "Seleccione un libro para ver mas detalles (o presione enter para continuar): "
            )
            if selected_book:
                display_user_book(USER.want_to_read_books[int(selected_book)])
    else:
        print("No tienes libros en tu lista")


# Search functions


def print_search_menu():
    print("1. Busqueda Simple")
    print("2. Busqueda Avanzada")
    print("3. Salir")


def print_simple_search():
    print("0. Todos")
    print("1. Titulo")
    print("2. Autor")
    print("3. Editora")
    print("4. Categoria")
    print("5. ISBN")
    print("6. LCCN")
    print("7. OCLC")





def display_book(book):
    print(f"Titulo: {book.title}")
    print(f"Autores: {book.authors}")
    print(f"Fecha de publicacion: {book.published_date}")
    print(f"Descripcion: {book.description}")
    print(f"Numero de paginas: {book.page_count}")
    print(f"Editora: {book.publisher}")
    print(f"Categorias: {book.categories}")
    print(f"Lenguaje: {book.language}")
    option = input("Desea añadirlo a su lista? (s/n): ")
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
    print(f"Se encontraron {books.number_of_books} libros")
    number_of_books = books.number_of_books
    number_of_books_displayed = 0
    while True:
        print_books(books.books)
        number_of_books_displayed += len(books.books)
        selected_book = input(
            "Seleccione un libro para ver mas detalles (o presione enter para continuar): "
        )
        if selected_book:
            display_book(books.books[int(selected_book)])
        if number_of_books_displayed < number_of_books:
            option = input("Desea ver mas libros? (s/n): ")
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
    search = input("Ingrese el termino de busqueda: ")
    print("Seleccione el campo por el cual desea buscar:")
    print_simple_search()
    search_type = int(input("Opcion: "))
    if search_type > 0:
        search_by_field = True
        search_type -= 1
        if search_type > 6:
            search_type = 0
        print(f"Buscando por {SearchType(search_type).name}")
    iterate_books(search, search_by_field=search_by_field, search_type=search_type)


def advanced_search():
    search_inputs = []
    search_inputs.append(
        input(
            "Ingrese el termino de busqueda (puede dejarlo vacio para buscar por cada campo): "
        )
    )
    print(
        "Ingrese el termino de busqueda por cada campo, si no desea buscar por un campo dejalo vacio:"
    )
    search_fields = SearchType.__members__.keys()
    for field in search_fields:
        search_inputs.append(input(f"{field}: "))
    iterate_books(search_inputs, advanced_search=True)


def search():
    print_search_menu()
    option = input("Opcion: ")
    if option == "1":
        simple_search()
    elif option == "2":
        advanced_search()
    else:
        print("Opcion no valida")


def no_gui_app():
    print("Bienvenido a Book App, pulse una de las siguientes opciones:")
    while True:
        print_menu()
        option = input("Opcion: ")
        if option == "1":
            my_books()
        elif option == "2":
            search()
        else:
            print("Saliendo...")
            break