from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from rng import rng_quote


class ChatBubbleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 14))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            "border-radius: 10px; padding: 10px; background-color: #FFFFFF; color: #000000;")


class ChatBubbleWindow(QMainWindow):
    def __init__(self, text):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.label = ChatBubbleLabel(text, self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = ChatBubbleWindow(rng_quote())
    window.show()
    app.exec_()
