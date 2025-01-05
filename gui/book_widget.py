from PyQt6 import QtCore, QtGui, QtWidgets
from gui.qelided_label import QElidedLabel
from model.book import Book


class BookWidget(QtWidgets.QWidget):
    main_window = None
    book: Book = None

    def __init__(self, main_window, book):
        super().__init__()
        self.main_window = main_window
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.book = book
        self.setMinimumSize(468, 72)
        self.setMaximumSize(468, 72)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.bookIcon = QtWidgets.QLabel(parent=self)
        self.bookIcon.setGeometry(QtCore.QRect(10, 10, 48, 72))
        self.bookIcon.setText("")
        self.bookIcon.setScaledContents(True)
        self.bookIcon.setObjectName("bookIcon")
        self.titleLabel = QElidedLabel(parent=self)
        self.titleLabel.setGeometry(QtCore.QRect(90, 10, 394, 21))
        self.titleLabel.setStyleSheet(
            'font: 600 12pt "Ubuntu Sans";\n' "color: rgb(0, 0, 0);"
        )
        self.titleLabel.setObjectName("titleLabel")
        self.authorLabel = QElidedLabel(parent=self)
        self.authorLabel.setGeometry(QtCore.QRect(90, 35, 394, 21))
        self.authorLabel.setStyleSheet(
            'font: 600 10pt "Ubuntu Sans";\n' "color: rgb(0, 0, 0);"
        )
        self.authorLabel.setObjectName("authorLabel")

        # Set book
        self.titleLabel.setText(book.title)
        self.authorLabel.setText(book.get_authors())

        if book.image:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(book.image.data)
            self.bookIcon.setPixmap(pixmap)
        else:
            self.bookIcon.setPixmap(QtGui.QPixmap("assets/icons8-reading-64.png"))

        self.events()

    def events(self):
        self.mousePressEvent = self.showBookFrame

    def showBookFrame(self, event):
        self.main_window.showBookFrame(self.book)
