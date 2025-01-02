from PyQt6 import QtCore, QtGui, QtWidgets
from utils.globals import SEARCH_TYPES, get_user_book_by_id
from api.search import search_books
from gui.book_widget import BookWidget

class SearchFrame(QtWidgets.QFrame):
    main_window = None

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

        self.events()

    def draw_ui(self):
        pass

    def events(self):
        self.searchButton.clicked.connect(lambda: self.search())

    def search(self):
        search = self.searchEdit.text()
        search_by_field = False
        search_type = self.searchTypeComboBox.currentIndex()
        if search_type > 0:
            search_by_field = True
            search_type -= 1
            if search_type > 6:
                search_type = 0

        books = search_books(search, search_by_field=search_by_field, search_type=search_type)

        # Add books to each grid layout removing the previous ones first
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        j = 0
        k = 0
        for book in books.books:
            if book:
                self.grid_layout.addWidget(BookWidget(self.main_window, book), j, k)
                k += 1
                if k == 2:
                    k = 0
                    j += 1