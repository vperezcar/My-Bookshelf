from PyQt6 import QtCore, QtGui, QtWidgets
from gui.user_book_widget import UserBookWidget
import utils.globals as globals


class BookPageFrame(QtWidgets.QFrame):
    main_window = None
    grid_layout: list = []
    tabObjectName: list = ["readTab", "readingTab", "wantToReadTab"]

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
        self.topFrame.setGeometry(QtCore.QRect(155, 15, 720, 90))
        self.topFrame.setStyleSheet("background-color: rgb(244, 242, 233);")
        self.topFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.topFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.topFrame.setObjectName("topFrame")
        self.readIcon = QtWidgets.QLabel(parent=self.topFrame)
        self.readIcon.setGeometry(QtCore.QRect(64, 13, 64, 64))
        self.readIcon.setText("")
        self.readIcon.setPixmap(QtGui.QPixmap("qt/../assets/icons8-reading-64.png"))
        self.readIcon.setScaledContents(True)
        self.readIcon.setObjectName("readIcon")
        self.booksLabel = QtWidgets.QLabel(parent=self.topFrame)
        self.booksLabel.setGeometry(QtCore.QRect(192, 30, 464, 30))
        self.booksLabel.setStyleSheet(
            'font: 600 20pt "Ubuntu Sans";\n' "color: rgb(0, 0, 0);"
        )
        self.booksLabel.setObjectName("booksLabel")
        self.userBookTab = QtWidgets.QTabWidget(parent=self)
        self.userBookTab.setGeometry(QtCore.QRect(15, 120, 1000, 495))
        self.userBookTab.setStyleSheet(
            "color: rgb(0, 0, 0);\n" 'font: 600 14pt "Ubuntu Sans";'
        )
        self.userBookTab.setObjectName("userBookTab")

        self.create_tab_widget()

        self.draw_ui()

        self.events()

    def create_tab_widget(self):
        self.tabs = []
        self.content_tab_widgets = []

        for tabName in self.tabObjectName:
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
        self.userBookTab.currentChanged.connect(self.update_book_label)

    def draw_ui(self):
        self.update_book_label()

        for i, tab in enumerate(self.tabs):
            self.userBookTab.setTabText(
                self.userBookTab.indexOf(tab), globals.USER_BOOK_TABS[i]
            )
            # Add books to each grid layout removing the previous ones first
            for j in reversed(range(self.grid_layout[i].count())):
                self.grid_layout[i].itemAt(j).widget().deleteLater()
            books = (
                globals.USER.read_books
                if i == 0
                else (
                    globals.USER.reading_books
                    if i == 1
                    else globals.USER.want_to_read_books
                )
            )
            if books:
                j = 0
                k = 0
                for book in books:
                    if book:
                        self.grid_layout[i].addWidget(
                            UserBookWidget(self.main_window, book), j, k
                        )
                        k += 1
                        if k == 2:
                            k = 0
                            j += 1

    def update_book_label(self):
        labelText = ""
        if self.userBookTab.currentIndex() == 0:
            labelText = f"Has leído {len(globals.USER.read_books)} "
        elif self.userBookTab.currentIndex() == 1:
            labelText = f"Estás leyendo {len(globals.USER.reading_books)} "
        else:
            labelText = f"Quieres leer {len(globals.USER.want_to_read_books)} "
        labelText += f"{'libros' if len(globals.USER.read_books) != 1 else 'libro'}"
        self.booksLabel.setText(labelText)
