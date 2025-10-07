import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLineEdit, QGraphicsScene, QGraphicsProxyWidget, QGraphicsView, QGraphicsItem
from PyQt6.QtGui import QPainter, QPen, QImage, QColor, QBrush

class Gpaphic(QWidget):
    def __init__(self, width = 600, height = 600):
        super().__init__()

        self.image = QImage(width, height, QImage.Format.Format_ARGB32)
        self.image.fill(QColor.fromString("#EFF9E8"))
        self.setFixedSize(QSize(width, height))

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

class MovableProxy(QGraphicsProxyWidget):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.offset = event.pos()
            self.dragging = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.MouseButton.RightButton) and self.dragging == True:
            new_pos = self.mapToScene(event.pos() - self.offset)
            self.setPos(new_pos)
            self.scene().update()
        else:
            self.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

class GrView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.scale_factor = 1.15

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom_in = self.scale_factor
            self.scale(zoom_in, zoom_in)
        else:
            zoom_out = 1/self.scale_factor
            self.scale(zoom_out, zoom_out)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget = QWidget()
        mainWidget.setMinimumHeight(700)
        mainWidget.setMinimumWidth(1150)
        mainWidget.setStyleSheet("background-color: #F5E2B0")

    #connect to an image class
        self.gr = Gpaphic()

    #All the labels:
        self.topLabel = QLabel("Simple function calculator")

    #1. scene:
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        #self.scene.setBackgroundBrush(QBrush(QColor("red")))
        self.scene.setBackgroundBrush(QBrush(QColor.fromString("#F5E2B0")))

    #2. proxy
        proxy = MovableProxy()
        proxy.setWidget(self.gr)
        imSize = self.gr.size()
        x = -imSize.width() / 2
        y = -imSize.height() / 2
        proxy.setPos(x,y)
        proxy.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(proxy)

    #view
        self.view = GrView(self.scene)
        self.view.centerOn(proxy)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFixedSize(QSize(700,650))
        self.view.setStyleSheet("border: 6px solid #C8A96A; border-radius: 10px;")

    #rightSide
        self.rightSide = QWidget()
    #its own stylesheet!
        self.rightSide.setObjectName("rightSide")
        self.rightSide.setStyleSheet("""
            QWidget#rightSide {
                border: 6px solid #C8A96A;
                border-radius: 10px;
            }
        """)

        self.rightSide.setMinimumSize(QSize(200,400))
        self.rightSide.setMaximumSize(QSize(350, 400))

        self.rightTopLabel = QLabel("Results")
        self.rightTopLabel.setStyleSheet("""
        QLabel {
        color: #C8A96A;
        font-size: 30px;
        font-weight: bold; 
        }""")

        self.x_Label = QLabel("x-intercepts:")
        self.x_Label.setStyleSheet("""
        QLabel {
        color: #C8A96A;
        font-size: 20px;
        font-weight: bold; 
        }
        """)

        self.x_resLabel = QLabel("(1;3)")
        self.x_resLabel.setStyleSheet("""
        QLabel {
                color: #C8A96A;
                font-size: 20px;
                font-weight: bold; 
                }
        """)

        self.y_Label = QLabel("x=y-intercepts:")
        self.y_Label.setStyleSheet("""
                QLabel {
                color: #C8A96A;
                font-size: 20px;
                font-weight: bold; 
                }
                """)

        self.y_resLabel = QLabel("(2:4)")
        self.y_resLabel.setStyleSheet("""
                        QLabel {
                        color: #C8A96A;
                        font-size: 20px;
                        font-weight: bold; 
                        }
                        """)

        rightLay = QVBoxLayout()
        rightLay.addWidget(self.rightTopLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        rightLay.addWidget(self.x_Label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addWidget(self.x_resLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addWidget(self.y_Label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addWidget(self.y_resLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.rightSide.setLayout(rightLay)


    #leftSide
        self.leftSide = QWidget()
    #its own style
        #self.leftSide.setStyleSheet("border: 6px solid #C8A96A; border-radius: 10px;")
        self.leftSide.setObjectName("leftSide")
        self.leftSide.setStyleSheet("""
                    QWidget#leftSide {
                        border: 6px solid #C8A96A;
                        border-radius: 10px;
                    }
                """)
        self.leftSide.setMinimumSize(QSize(200, 500))
        self.leftSide.setMaximumSize(QSize(350, 500))

        self.aLabel = QLabel("Enter a:")
        self.aEdit = QLineEdit

        self.bLabel = QLabel("Enter b:")
        self.bEdit = QLineEdit

        #horisontalLayout
        self.horisontalLayout = QHBoxLayout()
        self.horisontalLayout.addWidget(self.leftSide)
        self.horisontalLayout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.horisontalLayout.addWidget(self.rightSide)
        horWidget = QWidget()
        horWidget.setLayout(self.horisontalLayout)

    #mainLayout:
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.topLabel)
        mainLayout.addWidget(horWidget)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()