#!/home/rontero/Documents/Program-Files/miniconda3/bin/python3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from internet import fetch_news
from outlinelabel import OutlineLabel
from personality import get_response
from sticky import StickyNotes
from bubble import ChatBubbleWindow
from rng import rng_range, rng_choice
from gpt3mikoapi import predict, Model
from enum import IntEnum
import re

class Modes(IntEnum):
    NORMAL = 1
    SILENT = 2
    TALK = 4

class MikoWindow(QMainWindow):
    SPD = 25

    isBeingDragged = False
    canMove = True

    labels = []
    noteapp = StickyNotes()

    def __init__(self, mode: Modes = Modes.NORMAL):
        super().__init__()
        self.mode = mode
        self.bubble = ChatBubbleWindow("")

        news_themes = ["video games", "politics", "sports", "science",
                       "technology", "entertainment", "business", "health"]

        self.news = fetch_news(rng_choice(news_themes))
        self.newsIndex = 0

        self.name = get_response("#getName.capitalize#")

        # Tell window manager to ignore this window
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.mascotLabel = self.create_label(
            "Miku", self.mousePressEvent, visible=True, addToLabels=False, clickType=Qt.RightButton | Qt.LeftButton)
        self.mascotLabel.mouseReleaseEvent = self.mouseReleaseEvent

        self.mascotImage = QPixmap("mascot.png")
        mascotHeight, mascotWidth = self.mascotImage.height(), self.mascotImage.width()

        self.mascotLabel.setPixmap(self.mascotImage)
        self.mascotLabel.setGeometry(0, 0, mascotWidth, mascotHeight)

        self.create_label("Sticky Notes", self.open_notes)
        self.create_label("Speak", self.speak)
        self.create_label("News", self.open_news)
        self.create_label("Coin Flip", self.flip_coin)
        self.create_label(Modes(mode).name, self.change_mode)

        self.WIDTH = QApplication.desktop().screenGeometry().width()
        self.HEIGHT = QApplication.desktop().screenGeometry().height()

        self.setGeometry(0, 0, mascotWidth, mascotHeight)
        self.move(self.WIDTH // 2, self.HEIGHT // 2)
        self.move_window()

        QTimer.singleShot(5000, self.introduction)

    def change_mode(self, _):
        self.mode = Modes(self.mode * 2 % 2 ** len(Modes) or 1)
        self.labels[-1].setText(Modes(self.mode).name)
        if self.mode == Modes.SILENT:
            self.bubble.hide()
        elif self.mode == Modes.TALK:
            self.say("Hello")
        elif self.mode == Modes.NORMAL:
            self.introduction()

    def introduction(self):
        self.say(get_response(f"[name:{self.name}]#salutation#, \n#goodbye#"))
        QTimer.singleShot(45_000, self.idle_say)

    def idle_say(self):
        waitTime = self.speak(None)
        QTimer.singleShot(waitTime + 45_000, self.idle_say)

    def flip_coin(self, _):
        self.say("Heads" if rng_range(0, 1) == 0 else "Tails")

    def create_label(self, text, action, visible=False, addToLabels=True, clickType=Qt.LeftButton):
        label = OutlineLabel(text, self)
        label.setFont(QFont("Arial", 15))
        label.setBrush(Qt.yellow)

        def action_wrapper(event):
            if event.button() & clickType:
                action(event)
                if clickType == Qt.LeftButton:
                    self.toggle_labels(event)

        label.enterEvent = lambda _: label.setFont(QFont("Arial", 18))
        label.leaveEvent = lambda _: label.setFont(QFont("Arial", 15))

        label.mousePressEvent = action_wrapper
        label.setVisible(visible)

        if addToLabels:
            label.move(0, 25 * len(self.labels))
            self.labels.append(label)
        return label

    def open_notes(self, _):
        self.noteapp.mainloop()
        self.noteapp = StickyNotes()

    def say(self, text):
        PROMPT = "Reformat and summarize the following text with no more than 32 words, and no less than 16 words, keep the same POV:\n\n"
        prediction = predict(PROMPT + text, Model.BABBAGE)
        text = re.sub(r"\n\s*\n", "\n", re.sub(r"[.;?!]", "\n", prediction)).strip()
        self.bubble.change_text(text)
        self.bubble.move(self.x() - self.bubble.label.width() // 2, self.y() - self.bubble.label.height())
        self.bubble.setVisible(True)
        if self.mode & (Modes.TALK | Modes.NORMAL):
            from voice import say_tts
            say_tts(text.replace("\n", ". "))
        waitTime = int(len(text) * 0.1 * 1000)
        QTimer.singleShot(waitTime, self.bubble.hide)
        return waitTime

    def open_news(self, _):
        title, desc = self.news[self.newsIndex]
        self.newsIndex = (self.newsIndex + 1) % len(self.news)
        self.say(f"Today's news are {title}...{desc}")

    def speak(self, _):
        if rng_range(0, 100) < 25 and len(self.noteapp.notes):
            _, tkText = rng_choice(self.noteapp.notes)
            text = "Remember " + self.noteapp.get_text(tkText)
        else:
            text = get_response(f"[name: {self.name}]#origin#")
        return self.say(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isBeingDragged = True
            self.canMove = False
            if rng_range(0, 100) < 5:
                self.speak(event)
        else:
            self.toggle_labels(event)

    def mouseMoveEvent(self, event):
        if self.isBeingDragged:
            self.move(event.globalX() - self.width() // 2,
                      event.globalY() - self.height() // 2)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isBeingDragged = False
            self.canMove = True

    def toggle_labels(self, _):
        self.canMove = not self.canMove
        for lab in self.labels:
            lab.setVisible(not lab.isVisible())

    def move_window(self):
        QTimer.singleShot(100, self.move_window)

        if not self.canMove:
            return

        x, y = self.x() + rng_range(self.SPD), self.y() + rng_range(self.SPD)

        if x < 0:
            x = 0
        elif x + self.width() > self.WIDTH:
            x = self.WIDTH - self.width()

        if y < 0:
            y = 0
        elif y + self.height() > self.HEIGHT:
            y = self.HEIGHT - self.height()

        self.move(x, y)


if __name__ == "__main__":
    from sys import argv

    try:
        MODE = 2 ** (int(argv[1]) - 1) if len(argv) > 1 else Modes.NORMAL
    except ValueError:
        print("\nTry: python mascot.py <mode>")
        print("\nModes:\n1: Normal\n2: Silent\n3: Talk\n")
        exit(1)

    print(f"Running in {Modes(MODE).name} mode")
    app = QApplication([])
    win = MikoWindow(MODE)

    win.show()
    app.exec_()
