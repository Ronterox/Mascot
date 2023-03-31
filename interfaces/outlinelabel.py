from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QBrush, QPen, QPainter, QPainterPath, QFontMetrics
from math import ceil

# Source: https://stackoverflow.com/questions/64290561/qlabel-correct-positioning-for-text-outline

# TODO: Optimize the drawing, by setting properties only on setText

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
        metrics = QFontMetrics(self.font())

        path = QPainterPath()
        font, height = self.font(), metrics.height()
        lines = self.text().splitlines()
        for i, line in enumerate(lines):
            path.addText(self.x(), i * height + height, font, line)

        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        self.pen.setWidthF(width * 2)
        qp.strokePath(path, self.pen)
        if 1 < self.brush.style() < 15:
            qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)
