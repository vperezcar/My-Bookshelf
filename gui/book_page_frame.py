from PyQt6 import QtCore, QtWidgets
from gui.user_book_widget import UserBookWidget
from utils.constants.constants import USER_BOOK_TABS, ORDER_BY_ARRAY
import utils.globals as globals
import utils.constants.constants as constants


class BookPageFrame(QtWidgets.QFrame):
    main_window = None
    grid_layout: list = []
    tab_object_names: list = ["readTab", "readingTab", "wantToReadTab"]
    filter_used: list = [4, 4, 4]

    def __init__(self, parent, objectName="pageFrame", visible=False):
        super().__init__(parent.mainFrame)
        self.main_window = parent
        self.setupUi(objectName, visible)

    def setupUi(self, objectName, visible):
        self.setGeometry(QtCore.QRect(0, 90, 1030, 630))
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName(objectName)
        self.setVisible(visible)
        self.topFrame = QtWidgets.QFrame(parent=self)
        self.topFrame.setGeometry(QtCore.QRect(15, 15, 1000, 90))
        self.topFrame.setStyleSheet("background-color: rgb(244, 242, 233);")
        self.topFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.topFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.topFrame.setObjectName("topFrame")
        self.booksLabel = QtWidgets.QLabel(parent=self.topFrame)
        self.booksLabel.setGeometry(QtCore.QRect(15, 30, 464, 30))
        self.booksLabel.setStyleSheet(
            'font: 600 20pt "Ubuntu Sans";\n' "color: rgb(0, 0, 0);"
        )
        self.booksLabel.setObjectName("booksLabel")
        self.orderByLabel = QtWidgets.QLabel(parent=self.topFrame)
        self.orderByLabel.setGeometry(QtCore.QRect(530, 30, 165, 30))
        self.orderByLabel.setStyleSheet(
            'font: 600 20pt "Ubuntu Sans";\n' "color: rgb(0, 0, 0);"
        )
        self.orderByLabel.setObjectName("orderByLabel")
        self.orderByLabel.setText(constants.ORDER_BY)
        self.orderByComboBox = QtWidgets.QComboBox(parent=self.topFrame)
        self.orderByComboBox.setGeometry(QtCore.QRect(710, 25, 275, 40))
        self.orderByComboBox.setStyleSheet(
            "background-color: rgb(63, 131, 99);\n" 'font: 14pt "Ubuntu Sans";'
        )
        self.orderByComboBox.setObjectName("orderByComboBox")
        self.orderByComboBox.setEditable(True)
        self.orderByComboBox.lineEdit().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.userBookTab = QtWidgets.QTabWidget(parent=self)
        self.userBookTab.setGeometry(QtCore.QRect(15, 120, 1000, 495))
        self.userBookTab.setStyleSheet(
            "color: rgb(0, 0, 0);\n" 'font: 600 14pt "Ubuntu Sans";'
        )
        self.userBookTab.setObjectName("userBookTab")

        self.create_tab_widget()

        self.add_ORDER_BY_ARRAY_items()
        self.orderByComboBox.setCurrentIndex(4)

        self.draw_ui()

        self.events()

    def create_tab_widget(self):
        self.tabs = []
        self.content_tab_widgets = []

        for tabName in self.tab_object_names:
            tab = QtWidgets.QScrollArea()
            tab.setObjectName(tabName)
            self.tabs.append(tab)
            self.userBookTab.addTab(tab, "")
            content_tab_widget = QtWidgets.QWidget()
            tab.setWidget(content_tab_widget)
            tab.setWidgetResizable(True)
            grid_layout = QtWidgets.QGridLayout(content_tab_widget)
            grid_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            self.grid_layout.append(grid_layout)

    def events(self):
        self.userBookTab.currentChanged.connect(self.switch_tab)
        self.orderByComboBox.currentIndexChanged.connect(self.ORDER_BY_ARRAY)

    def order_books(self, tab, user_books):
        ORDER_BY_ARRAY = self.filter_used[tab]
        if ORDER_BY_ARRAY == 0:
            return sorted(user_books, key=lambda user_books: user_books.book.title)
        elif ORDER_BY_ARRAY == 1:
            return sorted(user_books, key=lambda user_books: user_books.book.authors[0])
        elif ORDER_BY_ARRAY == 2:
            return sorted(
                user_books, key=lambda user_books: user_books.book.published_date
            )
        elif ORDER_BY_ARRAY == 3:
            return sorted(
                user_books,
                key=lambda user_books: user_books.book.page_count,
                reverse=True,
            )
        elif ORDER_BY_ARRAY == 4:
            return sorted(
                user_books, key=lambda user_books: user_books.update_date, reverse=True
            )
        elif ORDER_BY_ARRAY == 5:
            return sorted(
                user_books, key=lambda user_books: user_books.score, reverse=True
            )
        else:
            return list(
                filter(
                    lambda user_books: user_books.update_date.split("/")[2].split(" ")[
                        0
                    ]
                    == self.orderByComboBox.currentText(),
                    user_books,
                )
            )

    def add_ORDER_BY_ARRAY_items(self):
        self.orderByComboBox.blockSignals(True)
        self.orderByComboBox.clear()
        self.orderByComboBox.addItems(ORDER_BY_ARRAY)
        # Remove the last item if the read tab is not selected
        if self.userBookTab.currentIndex() != 0:
            self.orderByComboBox.removeItem(5)
        else:
            # Add the years to the combo box
            self.orderByComboBox.addItems(globals.USER.get_years_read_book())
        self.orderByComboBox.blockSignals(False)

    def ORDER_BY_ARRAY(self):
        self.filter_used[self.userBookTab.currentIndex()] = (
            self.orderByComboBox.currentIndex()
        )
        self.draw_ui()

    def draw_ui(self):
        self.update_book_label()

        for i, tab in enumerate(self.tabs):
            self.userBookTab.setTabText(
                self.userBookTab.indexOf(tab), USER_BOOK_TABS[i]
            )
            # Add books to each grid layout removing the previous ones first
            for j in reversed(range(self.grid_layout[i].count())):
                self.grid_layout[i].itemAt(j).widget().deleteLater()
            user_books = (
                globals.USER.read_books
                if i == 0
                else (
                    globals.USER.reading_books
                    if i == 1
                    else globals.USER.want_to_read_books
                )
            )
            # Order books
            user_books = self.order_books(i, user_books)

            if user_books:
                j = 0
                k = 0
                for user_book in user_books:
                    if user_book:
                        self.grid_layout[i].addWidget(
                            UserBookWidget(self.main_window, user_book), j, k
                        )
                        k += 1
                        if k == 2:
                            k = 0
                            j += 1

    def switch_tab(self):
        self.add_ORDER_BY_ARRAY_items()
        # Reset the filter to the value it was previously used
        self.orderByComboBox.blockSignals(True)
        self.orderByComboBox.setCurrentIndex(
            self.filter_used[self.userBookTab.currentIndex()]
        )
        self.orderByComboBox.blockSignals(False)
        self.update_book_label()

    def update_book_label(self):
        labelText = ""
        books = None
        if self.userBookTab.currentIndex() == 0:
            labelText = f"{constants.HAS_READ} {len(globals.USER.read_books)} "
            books = globals.USER.read_books
        elif self.userBookTab.currentIndex() == 1:
            labelText = f"{constants.ARE_READING} {len(globals.USER.reading_books)} "
            books = globals.USER.reading_books
        else:
            labelText = (
                f"{constants.WANT_TO_READ} {len(globals.USER.want_to_read_books)} "
            )
            books = globals.USER.want_to_read_books
        labelText += f"{constants.BOOKS if len(books) != 1 or len(books) == 0 else constants.BOOK}{constants.IN_TOTAL if self.userBookTab.currentIndex() == 0 else ''}"
        self.booksLabel.setText(labelText)
