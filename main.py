import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QPainter, QPen, QImage, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget = QWidget()
        mainWidget.setMinimumHeight(700)
        mainWidget.setMinimumWidth(1000)
        mainWidget.setStyleSheet("background-color: #F5E2B0")

        self.topLabel = QLabel("Simple function calculator")

        self.image = QImage(500, 700, QImage.Format.Format_ARGB32)
        self.image.fill(QColor("white"))

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.image)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()