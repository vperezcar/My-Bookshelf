from PyQt6 import QtCore, QtGui, QtWidgets
from gui.qelided_label import QElidedLabel
from model.user import UserBook

class UserBookWidget(QtWidgets.QWidget):
    main_window = None
    user_book: UserBook = None
    score_icons: list = []
    score_icons_position: list = [QtCore.QRect(10, 115, 32, 32), QtCore.QRect(50, 115, 32, 32), QtCore.QRect(90, 115, 32, 32), QtCore.QRect(130, 115, 32, 32), QtCore.QRect(170, 115, 32, 32)]
    score_icons_name: list = ["scoreIcon1", "scoreIcon2", "scoreIcon3", "scoreIcon4", "scoreIcon5"]

    def __init__(self, main_window, user_book):
        super().__init__()
        self.main_window = main_window
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.user_book = user_book
        self.setMinimumSize(468, 154)
        self.setMaximumSize(468, 154)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.bookIcon = QtWidgets.QLabel(parent=self)
        self.bookIcon.setGeometry(QtCore.QRect(10, 10, 64, 97))
        self.bookIcon.setText("")
        self.bookIcon.setScaledContents(True)
        self.bookIcon.setObjectName("bookIcon")
        self.titleLabel = QElidedLabel(parent=self)
        self.titleLabel.setGeometry(QtCore.QRect(90, 10, 394, 21))
        self.titleLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.titleLabel.setObjectName("titleLabel")
        self.authorLabel = QElidedLabel(parent=self)
        self.authorLabel.setGeometry(QtCore.QRect(90, 35, 394, 21))
        self.authorLabel.setStyleSheet("font: 600 10pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.authorLabel.setObjectName("authorLabel")
        self.publishedLabel = QElidedLabel(parent=self)
        self.publishedLabel.setGeometry(QtCore.QRect(90, 60, 394, 21))
        self.publishedLabel.setStyleSheet("font: 600 10pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.publishedLabel.setObjectName("publishedLabel")
        self.pagesLabel = QElidedLabel(parent=self)
        self.pagesLabel.setGeometry(QtCore.QRect(90, 85, 394, 21))
        self.pagesLabel.setStyleSheet("font: 600 10pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.pagesLabel.setObjectName("publishedLabel")

        for i in range(5):
            star = QtWidgets.QLabel(parent=self)
            star.setGeometry(self.score_icons_position[i])
            star.setPixmap(QtGui.QPixmap("qt/../assets/icons8-star-32.png"))
            star.setText("")
            star.setScaledContents(True)
            star.setObjectName(self.score_icons_name[i])
            if user_book.score == 0:
                star.hide()
            elif user_book.score <= i:
                star.setPixmap(QtGui.QPixmap("qt/../assets/icons8-grey-star-32.png"))

        # Set user book
        self.titleLabel.setText(user_book.book.title)
        self.authorLabel.setText(user_book.book.get_authors())
        self.publishedLabel.setText(user_book.book.get_published_date())
        self.pagesLabel.setText(user_book.book.get_number_of_pages())
        if user_book.book.image:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(user_book.book.image.data)
            self.bookIcon.setPixmap(pixmap)
        else:
            self.bookIcon.setPixmap(QtGui.QPixmap("qt/../assets/icons8-reading-64.png"))

        self.events()

    def events(self):
        self.mousePressEvent = self.showBookFrame

    def showBookFrame(self, event):
        self.main_window.showBookFrame(self.user_book)