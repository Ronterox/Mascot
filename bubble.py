from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ChatBubbleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 14))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border-radius: 10px; padding: 10px; color: #FFFFFF;")


class ChatBubbleWindow(QMainWindow):
    def __init__(self, text):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.label = ChatBubbleLabel(text, self)
        self.timer = None

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.change_text(text)
    
    def change_text(self, text):
        self.label.setText("")
        if self.timer != None:
            self.killTimer(self.timer)
        self.text = text
        self.timer = self.startTimer(35)
        self.counter = 0
        
    def timerEvent(self, _e):
        if self.counter < len(self.text):
            self.counter += 1
            self.label.setText(self.text[:self.counter])
        else:
            self.killTimer(self.timer)
            self.timer = None


if __name__ == "__main__":
    app = QApplication([])
    win = ChatBubbleWindow("Words words words")
    win.show()
    app.exec_()
