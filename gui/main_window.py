from PyQt6 import QtCore, QtGui, QtWidgets
from gui.book_page_frame import BookPageFrame
from gui.user_book_frame import UserBookFrame
from gui.search_frame import SearchFrame
from model.user import UserBook
from utils.globals import MAIN_OPTIONS, get_user_book_by_id

class MainWindow(QtWidgets.QMainWindow):
    last_frame_position = 0

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 720)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.sideMenuFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.sideMenuFrame.setGeometry(QtCore.QRect(0, 0, 250, 720))
        self.sideMenuFrame.setStyleSheet("background-color: rgb(244, 242, 233);")
        self.sideMenuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sideMenuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sideMenuFrame.setObjectName("sideMenuFrame")
        self.myBookButton = QtWidgets.QPushButton(parent=self.sideMenuFrame)
        self.myBookButton.setGeometry(QtCore.QRect(30, 150, 201, 81))
        self.myBookButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 20pt \"Ubuntu Sans\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qt/../assets/icons8-book-shelf-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.myBookButton.setIcon(icon)
        self.myBookButton.setIconSize(QtCore.QSize(32, 32))
        self.myBookButton.setObjectName("myBookButton")
        self.myBookButton.clicked.connect(lambda: self.switchPage(0))

        self.titleLabel = QtWidgets.QLabel(parent=self.sideMenuFrame)
        self.titleLabel.setGeometry(QtCore.QRect(30, 20, 181, 71))
        self.titleLabel.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 600 22pt \"Ubuntu Sans\";")
        self.titleLabel.setObjectName("titleLabel")
        self.mySearchButton = QtWidgets.QPushButton(parent=self.sideMenuFrame)
        self.mySearchButton.setGeometry(QtCore.QRect(30, 250, 201, 81))
        self.mySearchButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 20pt \"Ubuntu Sans\";")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("qt/../assets/icons8-search-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.mySearchButton.setIcon(icon1)
        self.mySearchButton.setIconSize(QtCore.QSize(32, 32))
        self.mySearchButton.setObjectName("mySearchButton")
        self.mySearchButton.clicked.connect(lambda: self.switchPage(1))

        self.mainFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.mainFrame.setGeometry(QtCore.QRect(250, 0, 1030, 720))
        self.mainFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame.setObjectName("mainFrame")

        self.backButton = QtWidgets.QPushButton(parent=self.mainFrame)
        self.backButton.setGeometry(QtCore.QRect(13, 13, 64, 64))
        self.backButton.setStyleSheet("color: rgb(0, 0, 0);\n"
            "font: 20pt \"Ubuntu Sans\";\n"
            "\n"
            " background-color: white;\n"
            " border-style: solid;\n"
            " border-width:1px;\n"
            " border-radius:50px;")
        self.backButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("qt/../assets/icons8-back-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.backButton.setIcon(icon2)
        self.backButton.setIconSize(QtCore.QSize(32, 32))
        self.backButton.setObjectName("backButton")
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.backButton.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.backButton.hide()

        self.sectionLabel = QtWidgets.QLabel(parent=self.mainFrame)
        self.sectionLabel.setGeometry(QtCore.QRect(90, 0, 925, 90))
        self.sectionLabel.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 600 22pt \"Ubuntu Sans\";")
        self.sectionLabel.setObjectName("sectionLabel")

        # List of frames used to display the main window, only one is visible at a time
        self.frames = []
        self.frames.append(BookPageFrame(self, "bookPageFrame", True))
        self.frames.append(SearchFrame(self, "searchFrame", False))

        # Frame used to display the book information
        self.userBookFrame = UserBookFrame(self, "userBookFrame", False)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("My Book App")
        self.myBookButton.setText("Mis Libros")
        self.titleLabel.setText("My Book App")
        self.mySearchButton.setText("Búsqueda")
        self.sectionLabel.setText("Mis Libros")

    def switchPage(self, position):
        self.backButton.setVisible(False)
        self.userBookFrame.setVisible(False)
        for i, frame in enumerate(self.frames):
            frame.setVisible(i == position)
            if i == position:
                self.last_frame_position = i
                frame.draw_ui()
        self.sectionLabel.setText(MAIN_OPTIONS[position])

    def showBookFrame(self, book):
        # Check if the book is an instance of User
        if isinstance(book, UserBook):
            user_book = book
        else:
            user_book = get_user_book_by_id(book.id)
            if not user_book:
                user_book = book
        self.backButton.setVisible(True)
        self.backButton.clicked.connect(lambda: self.switchPage(self.last_frame_position))
        for frame in self.frames:
            frame.setVisible(False)
        if isinstance(user_book, UserBook):
            self.sectionLabel.setText(user_book.book.title)
            self.userBookFrame.display_book_information(user_book)
        else:
            self.sectionLabel.setText(user_book.title)
            self.userBookFrame.display_book_information(user_book)
        self.userBookFrame.setVisible(True)