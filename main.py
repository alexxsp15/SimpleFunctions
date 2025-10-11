import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLineEdit, QGraphicsScene, QGraphicsProxyWidget, QGraphicsView, QGraphicsItem
from PyQt6.QtGui import QPainter, QPen, QImage, QColor, QBrush
from calculations import calculate_axes_intersections, calculate_limits, transform_values

class Gpaphic(QWidget):
    def __init__(self, width = 600, height = 600):
        super().__init__()
        self.a = None
        self.b = None
        self.c = None

        self.image = QImage(width, height, QImage.Format.Format_ARGB32)
        self.image.fill(QColor.fromString("#EFF9E8"))
        self.setFixedSize(QSize(width, height))
        self.draw_grid()
        self.draw_axes()

    def draw_grid(self):
        imgPainter = QPainter(self.image)
        pen = QPen(QColor.fromString("#A1BEAF"))
        pen.setWidth(2)
        imgPainter.setPen(pen)
        for i in range(601):
            if i == 0:
                imgPainter.drawLine(i, 0, i, 600)
            elif i % 25 == 0:
                imgPainter.drawLine(i, 0, i, 600)
        for i in range(601):
            if i == 0:
                imgPainter.drawLine(0, i, 600, i)
            elif i % 25 == 0:
                imgPainter.drawLine(0, i, 600, i)

    def draw_axes(self):
        imgPainter = QPainter(self.image)
        # Ox Oy
        pen = QPen(QColor.fromString("#3A4E40"))
        pen.setWidth(2)
        imgPainter.setPen(pen)
        # --->
        imgPainter.drawLine(20, 300, 570, 300)
        imgPainter.drawLine(550, 292, 570, 300)
        imgPainter.drawLine(550, 308, 570, 300)
        # ^
        # |
        imgPainter.drawLine(300, 20, 300, 570)
        imgPainter.drawLine(308, 40, 300, 20)
        imgPainter.drawLine(292, 40, 300, 20)

    def draw_graph(self, points_list):
        imgPainter = QPainter(self.image)
        # Ox Oy
        pen = QPen(QColor.fromString("#3A4E40"))
        pen.setWidth(2)
        imgPainter.setPen(pen)

        imgPainter.drawLine(points_list[0], points_list[1])
        self.update()

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
        self.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.scale_factor = 1.1
        self.current_scale = 1

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom_in = self.scale_factor
            cscale = self.current_scale
            cscale = self.current_scale + zoom_in
            print(cscale)
            if cscale > 6:
                pass
            else:
                self.scale(zoom_in, zoom_in)
                self.current_scale = cscale
        else:
            zoom_out = 1/self.scale_factor
            cscale = self.current_scale
            cscale = self.current_scale - zoom_out
            print(cscale)
            if cscale < -6:
                pass
            else:
                self.scale(zoom_out, zoom_out)
                self.current_scale = cscale

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget = QWidget()
        mainWidget.setMinimumHeight(750)
        mainWidget.setMinimumWidth(1150)
        mainWidget.setStyleSheet("background-color: #F5E2B0")

    #connect to an image class
        self.gr = Gpaphic()

    #TopLabel:
        self.topLabel = QLabel("Simple function calculator")
        self.topLabel.setStyleSheet("""
        QLabel {
        font-size: 40px;
        color: #C8A96A;
        font-weight: bold;
        }
        """)

    #1. scene:
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
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

        self.rightSide.setMinimumSize(QSize(200,300))
        self.rightSide.setMaximumSize(QSize(350, 300))

        self.rightTopLabel = QLabel("Results")
        self.rightTopLabel.setStyleSheet("""
        QLabel {
        color: #C8A96A;
        font-size: 30px;
        font-weight: bold; 
        }""")

    #x-stuff
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

    #y-stuff
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
        rightLay.addStretch()
        rightLay.addWidget(self.x_Label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addWidget(self.x_resLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addStretch()
        rightLay.addWidget(self.y_Label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        rightLay.addWidget(self.y_resLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.rightSide.setLayout(rightLay)


    #leftSide
        self.leftSide = QWidget()
    #its own style
        self.leftSide.setObjectName("leftSide")
        self.leftSide.setStyleSheet("""
                    QWidget#leftSide {
                        border: 6px solid #C8A96A;
                        border-radius: 10px;
                    }
                """)
        self.leftSide.setMinimumSize(QSize(200, 500))
        self.leftSide.setMaximumSize(QSize(350, 500))

        self.leftTopLabel = QLabel("Input")
        self.leftTopLabel.setStyleSheet("""
        QLabel {
        color: #C8A96A;
        font-size: 30px;
        font-weight: bold; 
        }""")

    #a-stuff
        self.aLabel = QLabel("Enter a:")
        self.aLabel.setStyleSheet("""
        QLabel {
                color: #C8A96A;
                font-size: 20px;
                font-weight: bold; 
                }
        """)

        self.aEdit = QLineEdit()
        self.aEdit.setStyleSheet("""
        QLineEdit {
        background-color: #F5E2B0;
        border: 3px solid #E2C983;
        font-size: 12px;
        font-weight: bold;
        color: #A7874B;
        border-radius: 5px;
        }
        QLineEdit:focus {
        color: #A7874B;
        border: 3px solid #A7874B;
        }
        """)

    #b-stuff
        self.bLabel = QLabel("Enter b:")
        self.bLabel.setStyleSheet("""
                QLabel {
                        color: #C8A96A;
                        font-size: 20px;
                        font-weight: bold; 
                        }
                """)

        self.bEdit = QLineEdit()
        self.bEdit.setStyleSheet("""
                QLineEdit {
                background-color: #F5E2B0;
                border: 3px solid #E2C983;
                font-size: 12px;
                font-weight: bold;
                color: #A7874B;
                border-radius: 5px;
                }
                QLineEdit:focus {
                color: #A7874B;
                border: 3px solid #A7874B;
                }
                """)
    #c-stuff
        self.cLabel = QLabel("Enter c:")
        self.cLabel.setStyleSheet("""
                        QLabel {
                                color: #C8A96A;
                                font-size: 20px;
                                font-weight: bold; 
                                }
                        """)

        self.cEdit = QLineEdit()
        self.cEdit.setStyleSheet("""
                        QLineEdit {
                        background-color: #F5E2B0;
                        border: 3px solid #E2C983;
                        font-size: 12px;
                        font-weight: bold;
                        color: #A7874B;
                        border-radius: 5px;
                        }
                        QLineEdit:focus {
                        color: #A7874B;
                        border: 3px solid #A7874B;
                        }
                        """)

    #prolem showing
        self.problemLabel = QLabel("Your problem is:")
        self.problemLabel.setStyleSheet("""
                QLabel {
                        color: #C8A96A;
                        font-size: 20px;
                        font-weight: bold; 
                        }
                """)

        self.problem = QLabel("ax + by = c")
        self.problem.setStyleSheet("""
                QLabel {
                        color: #C8A96A;
                        font-size: 20px;
                        font-weight: bold; 
                        }
                """)

        self.okButton = QPushButton("Paint!")
        self.okButton.setMaximumWidth(100)
        self.okButton.setStyleSheet("""
        QPushButton {
        background-color: #F5E2B0;
        color: #C8A96A;
        font-size: 20px;
        font-weight: bold; 
        border: 3px solid #E2C983;
        border-radius: 5px;
        }
        QPushButton:pressed {
        background-color: #E2C983;
        border: 3px solid #A7874B;
        color: #A7874B;
        }""")
        self.okButton.clicked.connect(self.paint_pressed)

    #lineEdits connect
        self.aEdit.textChanged.connect(self.show_problem)
        self.bEdit.textChanged.connect(self.show_problem)
        self.cEdit.textChanged.connect(self.show_problem)

        leftLay = QVBoxLayout()
        leftLay.addWidget(self.leftTopLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        leftLay.addStretch()
        leftLay.addWidget(self.aLabel)
        leftLay.addWidget(self.aEdit)
        leftLay.addStretch()
        leftLay.addWidget(self.bLabel)
        leftLay.addWidget(self.bEdit)
        leftLay.addStretch()
        leftLay.addWidget(self.cLabel)
        leftLay.addWidget(self.cEdit)
        leftLay.addStretch()
        leftLay.addWidget(self.problemLabel)
        leftLay.addWidget(self.problem, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        leftLay.addStretch()
        leftLay.addWidget(self.okButton, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.leftSide.setLayout(leftLay)

        #horisontalLayout
        self.horisontalLayout = QHBoxLayout()
        self.horisontalLayout.addWidget(self.leftSide)
        self.horisontalLayout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.horisontalLayout.addWidget(self.rightSide)
        horWidget = QWidget()
        horWidget.setLayout(self.horisontalLayout)

    #mainLayout:
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.topLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        mainLayout.addWidget(horWidget)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    def show_problem(self):
        a_text = self.aEdit.text().strip()
        b_text = self.bEdit.text().strip()
        c_text = self.cEdit.text().strip()

        def safe_float(value):
            try:
                return float(value)
            except ValueError:
                return None

        a = safe_float(a_text)
        b = safe_float(b_text)
        c = safe_float(c_text)

        if a is None or b is None or c is None:
            self.problem.setText("Невірний формат")
            return

        if a == 0:
            self.problem.setText(f"{b}y = {c}")
        elif b == 0:
            self.problem.setText(f"{a}x = {c}")
        elif b < 0:
            self.problem.setText(f"{a}x - {abs(b)}y = {c}")
        else:
            self.problem.setText(f"{a}x + {b}y = {c}")

    def paint_pressed(self):
        self.gr.a = float(self.aEdit.text())
        self.gr.b = float(self.bEdit.text())
        self.gr.c = float(self.cEdit.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()