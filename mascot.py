#!/home/rontero/Documents/Program-Files/miniconda3/bin/python3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from internet import fetch_news
from outlinelabel import OutlineLabel
from personality import get_response
from sticky import StickyNote
from bubble import ChatBubbleWindow
from rng import rng_range


class MikuWindow(QMainWindow):
    SPD = 25

    isBeingDragged = False
    canMove = True

    labels = []

    def __init__(self, bubble):
        super().__init__()

        from time import time
        news_themes = ["video games", "politics", "sports", "science", "technology", "entertainment", "business", "health"]

        self.news = fetch_news(news_themes[int(time() % len(news_themes))])
        self.newsIndex = 0

        self.name = get_response("#getName.capitalize#")
        self.bubble = bubble

        # Tell window manager to ignore this window
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.mascotLabel = self.create_label("Miku", self.mousePressEvent, visible=True, addToLabels=False, clickType=Qt.RightButton | Qt.LeftButton)
        self.mascotLabel.mouseReleaseEvent = self.mouseReleaseEvent

        self.mascotImage = QPixmap("mascot.png")
        mascotHeight, mascotWidth = self.mascotImage.height(), self.mascotImage.width()

        self.mascotLabel.setPixmap(self.mascotImage)
        self.mascotLabel.setGeometry(0, 0, mascotWidth, mascotHeight)

        self.create_label("Sticky Notes", self.open_notes)
        self.create_label("Quotes", self.say_quote)
        self.create_label("News", self.open_news)
        self.create_label("Introduction", self.introduction)
        self.create_label("Coin Flip", self.flip_coin)
        self.labels.append(self.bubble.label)

        self.WIDTH = QApplication.desktop().screenGeometry().width()
        self.HEIGHT = QApplication.desktop().screenGeometry().height()

        self.setGeometry(0, 0, mascotWidth, mascotHeight)
        self.move(self.WIDTH // 2, self.HEIGHT // 2)
        self.move_window()

        QTimer.singleShot(5000, self.idle_say)

    def introduction(self, _):
        self.say_something(get_response(f"[name:{self.name}]#salutation#, \n#goodbye#"))

    def idle_say(self):
        self.say_quote(None)
        QTimer.singleShot(45_000, self.idle_say)
    
    def flip_coin(self, _):
        self.say_something("Do it pussy" if rng_range(0, 1) == 0 else "Don't")

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
        StickyNote().mainloop()

    def say_something(self, text):
        from voice import say_tts
        self.bubble.change_text(text)
        self.bubble.move(self.x() - self.bubble.label.width() // 2, self.y() - self.bubble.label.height())
        self.bubble.setVisible(True)
        QTimer.singleShot(10000, self.bubble.hide)
        say_tts(text)

    def open_news(self, _):
        title, desc = self.news[self.newsIndex]
        saying = f"Today's news are {title}...{desc}"
        self.newsIndex = (self.newsIndex + 1) % len(self.news)
        self.say_something(saying)

    def say_quote(self, _):
        self.say_something(get_response(f"[name: {self.name}]#origin#"))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isBeingDragged = True
            self.canMove = False
            if rng_range(0, 100) < 5:
                self.say_quote(event)
        else:
            self.toggle_labels(event)
    
    def mouseMoveEvent(self, event):
        if self.isBeingDragged:
            self.move(event.globalX() - self.width() // 2, event.globalY() - self.height() // 2)
    
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
    app = QApplication([])
    win = MikuWindow(ChatBubbleWindow(""))
    win.show()
    app.exec_()
