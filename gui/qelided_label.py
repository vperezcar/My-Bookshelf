from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtWidgets


class QElidedLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(
            self.text(), Qt.TextElideMode.ElideRight, self.width()
        )

        painter.drawText(self.rect(), self.alignment(), elided)
