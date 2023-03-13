from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QBrush, QPen, QPainter, QPainterPath, QFontMetrics, QLinearGradient, QGradient, QRadialGradient, QColor, QPixmap
from math import ceil

# Source: https://stackoverflow.com/questions/64290561/qlabel-correct-positioning-for-text-outline
# TODO: Understand this code

class OutlineLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thickness = 1 / 25
        self.mode = True
        self.setBrush(Qt.white)
        self.setPen(Qt.black)
    
    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state

    def outlineThickness(self):
        return self.thickness * self.font().pointSize() if self.mode else self.thickness

    def setOutlineThickness(self, value):
        self.thickness = value

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            pen = QPen(pen)
        pen.setJoinStyle(Qt.RoundJoin)
        self.pen = pen

    def sizeHint(self):
        width = ceil(self.outlineThickness() * 2)
        return super().sizeHint() + QSize(width, width)

    def minimumSizeHint(self):
        width = ceil(self.outlineThickness() * 2)
        return super().minimumSizeHint() + QSize(width, width)

    def paintEvent(self, event):
        if self.text() == '':
            return super().paintEvent(event)
        width = int(self.outlineThickness())
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        tr = metrics.boundingRect(self.text()).adjusted(0, 0, width, width)
        if self.indent() == -1:
            indent = (metrics.boundingRect('x').width() + width * 2) / 2 if self.frameWidth() else width
        else:
            indent = self.indent()

        alignment = self.alignment()
        if alignment & Qt.AlignLeft:
            x = rect.left() + indent - min(metrics.leftBearing(self.text()[0]), 0)
        elif alignment & Qt.AlignRight:
            x = rect.x() + rect.width() - indent - tr.width()
        else:
            x = (rect.width() - tr.width()) / 2

        if alignment & Qt.AlignTop:
            y = rect.top() + indent + metrics.ascent()
        elif alignment & Qt.AlignBottom:
            y = rect.y() + rect.height() - indent - metrics.descent()
        else:
            y = (rect.height() + metrics.ascent() - metrics.descent()) / 2

        path = QPainterPath()
        font, height = self.font(), metrics.height()
        for i, line in enumerate(self.text().splitlines()):
            path.addText(x, int(y + (i * height) * 0.9), font, line)
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        self.pen.setWidthF(width * 2)
        qp.strokePath(path, self.pen)
        if 1 < self.brush.style() < 15:
            qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)


class Template(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout(self)
        text = 'Felicitations'

        label = OutlineLabel(text)
        linearGrad = QLinearGradient(0, 1, 0, 0)
        linearGrad.setCoordinateMode(QGradient.ObjectBoundingMode)
        linearGrad.setColorAt(0, QColor('#0fd850'))
        linearGrad.setColorAt(1, QColor('#f9f047'))
        label.setBrush(linearGrad)
        label.setPen(Qt.darkGreen)
        vbox.addWidget(label)

        label = OutlineLabel(text)
        radialGrad = QRadialGradient(0.3, 0.7, 0.05)
        radialGrad.setCoordinateMode(QGradient.ObjectBoundingMode)
        radialGrad.setSpread(QGradient.ReflectSpread)
        radialGrad.setColorAt(0, QColor('#0250c5'))
        radialGrad.setColorAt(1, QColor('#2575fc'))
        label.setBrush(radialGrad)
        label.setPen(QColor('Navy'))
        vbox.addWidget(label)

        label = OutlineLabel(text)
        linearGrad.setStart(0, 0)
        linearGrad.setFinalStop(1, 0)
        linearGrad.setColorAt(0, Qt.cyan)
        linearGrad.setColorAt(1, Qt.magenta)
        label.setPen(QPen(linearGrad, 1))  # pen width is ignored
        vbox.addWidget(label)

        label = OutlineLabel(text)
        linearGrad.setFinalStop(1, 1)
        for x in [(0, '#231557'), (0.29, '#44107A'), (0.67, '#FF1361'), (1, '#FFF800')]:
            linearGrad.setColorAt(x[0], QColor(x[1]))
        label.setBrush(linearGrad)
        label.setPen(QPen(QBrush(QColor('RoyalBlue'), Qt.Dense4Pattern), 1))
        label.setOutlineThickness(1 / 15)
        vbox.addWidget(label)

        label = OutlineLabel(text)
        label.setBrush(QBrush(Qt.darkBlue, Qt.BDiagPattern))
        label.setPen(Qt.darkGray)
        vbox.addWidget(label)

        label = OutlineLabel(text, styleSheet='background-color: black')
        # label.setBrush(QPixmap('paint.jpg'))
        label.setPen(QColor('Lavender'))
        vbox.addWidget(label)

        self.setStyleSheet('''
        OutlineLabel {
            font-family: Ubuntu;
            font-size: 60pt;
            font-weight: bold;
        }''')


if __name__ == '__main__':
    app = QApplication([])
    window = Template()
    window.show()
