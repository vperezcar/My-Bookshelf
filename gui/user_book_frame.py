from PyQt6 import QtCore, QtGui, QtWidgets
from model.user import UserBook, UserBookStatus
from utils.globals import USER_BOOK_TABS, update_user_book_status, update_user_book_score
import functools

class UserBookFrame(QtWidgets.QFrame):
    user_book: UserBook = None
    main_window = None
    score_icons: list = []
    score_icons_position: list = [QtCore.QRect(29, 290, 32, 32), QtCore.QRect(61, 290, 32, 32), QtCore.QRect(93, 290, 32, 32), QtCore.QRect(125, 290, 32, 32), QtCore.QRect(157, 290, 32, 32)]
    score_icons_name: list = ["scoreIcon1", "scoreIcon2", "scoreIcon3", "scoreIcon4", "scoreIcon5"]

    def __init__(self, parent, objectName="userBookFrame", visible=False):
        super().__init__(parent.mainFrame)
        self.main_window = parent
        self.setupUi(objectName, visible)

    def setupUi(self, objectName, visible):
        self.setGeometry(QtCore.QRect(0, 90, 1030, 630))
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName(objectName)
        self.setVisible(visible)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.bookIcon = QtWidgets.QLabel(parent=self.centralwidget)
        self.bookIcon.setGeometry(QtCore.QRect(45, 15, 128, 193))
        self.bookIcon.setText("")
        self.bookIcon.setPixmap(QtGui.QPixmap("qt/../assets/icons8-reading-64.png"))
        self.bookIcon.setScaledContents(True)
        self.bookIcon.setObjectName("bookIcon")
        self.selectorComboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.selectorComboBox.setGeometry(QtCore.QRect(15, 240, 188, 35))
        self.selectorComboBox.setStyleSheet("background-color: rgb(63, 131, 99);")
        self.selectorComboBox.setObjectName("selectorComboBox")
        self.selectorComboBox.addItems(USER_BOOK_TABS)
        self.selectorComboBox.setEditable(True)
        self.selectorComboBox.lineEdit().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.authorLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.authorLabel.setGeometry(QtCore.QRect(213, 15, 802, 20))
        self.authorLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.authorLabel.setObjectName("authorLabel")
        self.numberOfPagesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.numberOfPagesLabel.setGeometry(QtCore.QRect(213, 45, 802, 20))
        self.numberOfPagesLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.numberOfPagesLabel.setObjectName("numberOfPagesLabel")
        self.publishedDateLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.publishedDateLabel.setGeometry(QtCore.QRect(213, 75, 802, 20))
        self.publishedDateLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.publishedDateLabel.setObjectName("publishedDateLabel")
        self.publisherLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.publisherLabel.setGeometry(QtCore.QRect(213, 105, 802, 20))
        self.publisherLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.publisherLabel.setObjectName("publisherLabel")
        self.categoriesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.categoriesLabel.setGeometry(QtCore.QRect(213, 135, 802, 20))
        self.categoriesLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.categoriesLabel.setObjectName("categoriesLabel")
        self.languagesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.languagesLabel.setGeometry(QtCore.QRect(213, 165, 802, 20))
        self.languagesLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.languagesLabel.setObjectName("languagesLabel")

        scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        scrollArea.setGeometry(QtCore.QRect(213, 195, 802, 435))
        vBoxLayout = QtWidgets.QVBoxLayout()
        self.descriptionLabel = QtWidgets.QLabel()
        self.descriptionLabel.setStyleSheet("font: 600 12pt \"Ubuntu Sans\";\n"
"color: rgb(0, 0, 0);")
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionLabel.setWordWrap(True)
        vBoxLayout.addWidget(self.descriptionLabel)

        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.descriptionLabel)

        for i in range(5):
            star = QtWidgets.QLabel(parent=self)
            star.setGeometry(self.score_icons_position[i])
            star.setPixmap(QtGui.QPixmap("qt/../assets/icons8-star-32.png"))
            star.setText("")
            star.setScaledContents(True)
            star.setObjectName(self.score_icons_name[i])
            star.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.score_icons.append(star)

    def display_book_information(self, user_book):
        self.user_book = user_book
        self.authorLabel.setText(user_book.book.get_authors())
        self.descriptionLabel.setText(user_book.book.get_description())
        self.publisherLabel.setText(user_book.book.get_publisher())
        self.numberOfPagesLabel.setText(user_book.book.get_number_of_pages())
        self.publishedDateLabel.setText(user_book.book.get_published_date())
        self.categoriesLabel.setText(user_book.book.get_categories())
        self.languagesLabel.setText(user_book.book.get_language())

        if user_book.book.image:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(user_book.book.image.data)
            self.bookIcon.setPixmap(pixmap)
        else:
            self.bookIcon.setPixmap(QtGui.QPixmap("qt/../assets/icons8-reading-64.png"))

        self.selectorComboBox.setCurrentIndex(user_book.status.value)

        self.draw_review()

        self.events()

    def draw_review(self):
        for i in range(5):
            self.score_icons[i].setPixmap(QtGui.QPixmap("qt/../assets/icons8-star-32.png") if self.user_book.score > i else QtGui.QPixmap("qt/../assets/icons8-grey-star-32.png"))
            self.score_icons[i].setVisible(self.user_book.status.value == 0)

    def events(self):
        self.selectorComboBox.currentIndexChanged.connect(lambda: self.update_user_book_status(self.selectorComboBox.currentIndex()))

        for i in range(5):
            self.score_icons[i].mousePressEvent = functools.partial(self.update_user_book_score, score=i + 1)

    def update_user_book_status(self, status):
        if self.user_book.status.value != status:
            # Reset the score to zero if the status is not read
            if status != 0:
                self.user_book.score = 0
                update_user_book_score(self.user_book, 0)
            update_user_book_status(self.user_book, status)
            self.user_book.status = UserBookStatus(status)
            self.draw_review()

    def update_user_book_score(self, event, score):
        if self.user_book.score != score:
            update_user_book_score(self.user_book, score)
            self.user_book.score = score
            self.draw_review()