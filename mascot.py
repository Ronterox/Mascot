#!/home/rontero/Documents/Program-Files/miniconda3/bin/python3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from internet import fetch_news
from outlinelabel import OutlineLabel
from personality import get_response
from sticky import StickyNote
from bubble import ChatBubbleWindow
from rng import rng_range

class MikuWindow(QMainWindow):
    SPD = 25

    def __init__(self, bubble):
        super().__init__()
        self.labels = []

        self.news = fetch_news("video games")
        self.news_index = 0
        self.name = get_response("#getName.capitalize#")
        self.bubble = bubble

        # Tell window manager to ignore this window
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.can_move = True
        self.mascot_label = self.create_label("Miku", self.show_label, visible=True, addToLabels=False)

        self.mascot_image = QPixmap("mascot.png")
        mascotHeight, mascotWidth = self.mascot_image.height(), self.mascot_image.width()

        self.mascot_label.setPixmap(self.mascot_image)
        self.mascot_label.setGeometry(0, 0, mascotWidth, mascotHeight)

        self.create_label("Sticky Notes", self.open_notes)
        self.create_label("Quotes", self.open_quotes)
        self.create_label("News", self.open_news)
        self.create_label("Introduction", self.introduction)
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
        self.open_quotes(None)
        QTimer.singleShot(25_000, self.idle_say)

    def create_label(self, text, action, visible=False, addToLabels=True):
        label = OutlineLabel(text, self)
        label.setStyleSheet("QLabel {color: white;}")
        label.mousePressEvent = action
        label.enterEvent = self.toggle_move
        label.leaveEvent = self.toggle_move
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
        self.bubble.move(self.x() - self.bubble.label.width() //
                         2, self.y() - self.bubble.label.height())
        self.bubble.setVisible(True)
        QTimer.singleShot(10000, self.bubble.hide)
        say_tts(text)

    def open_news(self, _):
        title, desc = self.news[self.news_index]
        saying = f"Today's news are {title}...{desc}"
        self.news_index = (self.news_index + 1) % len(self.news)
        self.say_something(saying)

    def open_quotes(self, _):
        self.say_something(get_response(f"[name: {self.name}]#origin#"))

    def show_label(self, _):
        for lab in self.labels:
            lab.setVisible(not lab.isVisible())

    def toggle_move(self, _):
        self.can_move = not self.can_move

    def move_window(self):
        QTimer.singleShot(100, self.move_window)

        if not self.can_move:
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
