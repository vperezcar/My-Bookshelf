from PyQt6 import QtCore, QtGui, QtWidgets
from utils.globals import SEARCH_TYPES
from api.search import search_books
from gui.book_widget import BookWidget
import math
import re

class SearchFrame(QtWidgets.QFrame):
    main_window = None
    books = None
    page: int = 1
    number_of_books: int = -1
    cache_books: list = []

    def __init__(self, parent, objectName="searchFrame", visible=False):
        super().__init__(parent.mainFrame)
        self.main_window = parent
        self.setupUi(objectName, visible)

    def setupUi(self, objectName, visible):
        self.setGeometry(QtCore.QRect(0, 90, 1030, 630))
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName(objectName)
        self.setVisible(visible)
        self.searchButton = QtWidgets.QPushButton(parent=self)
        self.searchButton.setGeometry(QtCore.QRect(768, 50, 48, 48))
        self.searchButton.setStyleSheet("color: rgb(0, 0, 0);\n"
            "font: 20pt \"Ubuntu Sans\";\n"
            "\n"
            " background-color: white;\n"
            " border-style: solid;\n"
            " border-width:1px;\n"
            " border-radius:50px;")
        self.searchButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qt/../assets/icons8-search-32.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(32, 32))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.searchButton.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.searchEdit = QtWidgets.QLineEdit(parent=self)
        self.searchEdit.setGeometry(QtCore.QRect(256, 50, 512, 48))
        self.searchEdit.setStyleSheet("font: 14pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.searchEdit.setText("")
        self.searchEdit.setObjectName("searchEdit")
        self.searchTypeComboBox = QtWidgets.QComboBox(parent=self)
        self.searchTypeComboBox.setGeometry(QtCore.QRect(128, 50, 128, 48))
        self.searchTypeComboBox.setStyleSheet("background-color: rgb(63, 131, 99);\n"
"font: 14pt \"Ubuntu Sans\";")
        self.searchTypeComboBox.setObjectName("searchTypeComboBox")
        self.searchTypeComboBox.addItems(SEARCH_TYPES)
        self.searchTypeComboBox.setEditable(True)
        self.searchTypeComboBox.lineEdit().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.resultFrame = QtWidgets.QFrame(parent=self)
        self.resultFrame.setGeometry(QtCore.QRect(15, 120, 1000, 495))
        self.resultFrame.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 600 14pt \"Ubuntu Sans\";")
        self.resultFrame.setObjectName("resultFrame")

        self.grid_layout = QtWidgets.QGridLayout(self.resultFrame)
        self.grid_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.backResultButton = QtWidgets.QPushButton(parent=self)
        self.backResultButton.setGeometry(QtCore.QRect(857, 583, 32, 32))
        self.backResultButton.setStyleSheet("color: rgb(0, 0, 0);\n"
            "font: 20pt \"Ubuntu Sans\";\n"
            "\n"
            " background-color: white;\n"
            " border-style: solid;\n"
            " border-width:1px;\n"
            " border-radius:50px;")
        self.backResultButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("qt/../assets/icons8-back-24.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.backResultButton.setIcon(icon1)
        self.backResultButton.setIconSize(QtCore.QSize(32, 32))
        self.backResultButton.setObjectName("backResultButton")
        self.backResultButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.backResultButton.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.forwardResultButton = QtWidgets.QPushButton(parent=self)
        self.forwardResultButton.setGeometry(QtCore.QRect(983, 583, 32, 32))
        self.forwardResultButton.setStyleSheet("color: rgb(0, 0, 0);\n"
            "font: 20pt \"Ubuntu Sans\";\n"
            "\n"
            " background-color: white;\n"
            " border-style: solid;\n"
            " border-width:1px;\n"
            " border-radius:50px;")
        self.forwardResultButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("qt/../assets/icons8-forward-24.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.forwardResultButton.setIcon(icon2)
        self.forwardResultButton.setIconSize(QtCore.QSize(32, 32))
        self.forwardResultButton.setObjectName("forwardResultButton")
        self.forwardResultButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.forwardResultButton.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.pageResultEdit = QtWidgets.QLineEdit(parent=self)
        self.pageResultEdit.setGeometry(QtCore.QRect(904, 583, 64, 32))
        self.pageResultEdit.setStyleSheet("font: 14pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.pageResultEdit.setText("")
        self.pageResultEdit.setObjectName("pageResultEdit")
        self.pageResultEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.draw_ui()

        self.events()

    def draw_ui(self):
        self.backResultButton.setVisible(self.books != None)
        self.forwardResultButton.setVisible(self.books != None)
        self.pageResultEdit.setVisible(self.books != None)

    def events(self):
        self.searchButton.clicked.connect(lambda: self.search())
        self.backResultButton.clicked.connect(lambda: self.update_page(self.page - 1))
        self.forwardResultButton.clicked.connect(lambda: self.update_page(self.page + 1))

        self.pageResultEdit.textChanged.connect(lambda: self.update_page(self.get_page_from_edit()))

    def get_page_from_edit(self):
        result_string = re.sub("[^0-9/]", "", self.pageResultEdit.text())
        match = re.search(r"[0-9]+/[0-9]+", result_string)
        if match:
            return int(match.group().split("/")[0])
        else:
            self.pageResultEdit.blockSignals(True)
            self.pageResultEdit.setText(f"{self.page}/{math.floor(self.number_of_books/10)}")
            self.pageResultEdit.blockSignals(False)
            return self.page

    def update_page(self, page):
        if page >= 1 and page <= math.floor(self.number_of_books/10):
            self.page = page
            self.search()

    def search(self):
        search = self.searchEdit.text()
        search_by_field = False
        search_type = self.searchTypeComboBox.currentIndex()
        if search_type > 0:
            search_by_field = True
            search_type -= 1
            if search_type > 6:
                search_type = 0

        if not self.cache_books or self.cache_books[(self.page - 1) * 10] == None:
            # skip search if we got the books already
            self.books = search_books(search, search_by_field=search_by_field, search_type=search_type, start_index=(self.page - 1) * 10)
        else:
            self.books.books = self.cache_books[(self.page - 1) * 10:self.page * 10]

        if self.number_of_books == -1:
            self.number_of_books = self.books.number_of_books
            self.cache_books = [None] * self.number_of_books

        # Add books to each grid layout removing the previous ones first
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        j = 0
        k = 0
        for index, book in enumerate(self.books.books):
            if book:
                self.cache_books[index + (self.page - 1) * 10] = book
                self.grid_layout.addWidget(BookWidget(self.main_window, book), j, k)
                k += 1
                if k == 2:
                    k = 0
                    j += 1

        self.pageResultEdit.blockSignals(True)
        self.pageResultEdit.setText(f"{self.page}/{math.floor(self.number_of_books/10)}")
        self.pageResultEdit.blockSignals(False)
        self.draw_ui()