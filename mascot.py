#!/usr/bin/python3
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from sticky import StickyNote
from bubble import ChatBubbleWindow
from rng import rng_quote, rng_range


class MikuWindow(QMainWindow):
    SPD = 25

    def __init__(self, bubble):
        super().__init__()

        self.bubble = bubble

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.can_move = True
        self.mascot_label = self.create_label("Miku", self.show_label, True)

        self.mascot_image = QPixmap("mascot.png")
        mheight, mwidth = self.mascot_image.height(), self.mascot_image.width()

        self.mascot_label.setPixmap(self.mascot_image)
        self.mascot_label.setGeometry(0, 0, mwidth, mheight)

        hello_label = self.create_label("Sticky Notes", self.open_notes)
        quote_label = self.create_label("Quotes", self.open_quotes)
        quote_label.move(0, 25)

        self.labels = [hello_label, quote_label, self.bubble]

        self.WIDTH = QApplication.desktop().screenGeometry().width()
        self.HEIGHT = QApplication.desktop().screenGeometry().height()

        self.setGeometry(0, 0, mwidth, mheight)

        self.move(self.WIDTH // 2, self.HEIGHT // 2)
        self.move_window()

    def create_label(self, text, action, visible=False):
        label = QLabel(text, self)
        label.setStyleSheet("QLabel {color: white;}")
        label.mousePressEvent = action
        label.enterEvent = self.toggle_move
        label.leaveEvent = self.toggle_move
        label.setVisible(visible)
        return label

    def open_notes(self, _e):
        StickyNote().mainloop()

    def open_quotes(self, _e):
        self.bubble.label.setText(rng_quote())
        self.bubble.setVisible(False)
        self.bubble.setVisible(True)

    def show_label(self, _e):
        for lab in self.labels:
            lab.setVisible(not lab.isVisible())

    def toggle_move(self, _e):
        self.can_move = not self.can_move

    def move_window(self):
        QTimer.singleShot(100, self.move_window)

        if not self.can_move:
            return

        x, y = self.x() + rng_range(self.SPD), \
            self.y() + rng_range(self.SPD)

        if x < 0:
            x = 0
        elif x + self.width() > self.WIDTH:
            x = self.WIDTH - self.width()
        if y < 0:
            y = 0
        elif y + self.height() > self.HEIGHT:
            y = self.HEIGHT - self.height()

        self.move(x, y)
        self.bubble.move(x - self.bubble.label.width() //
                         2, y - self.bubble.label.height())


if __name__ == "__main__":
    app = QApplication([])
    MikuWindow(ChatBubbleWindow(rng_quote())).show()
    app.exec_()
