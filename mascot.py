from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from internet import fetch_news
from personality import get_response
from sticky import StickyNote
from bubble import ChatBubbleWindow
from rng import rng_range


class MikuWindow(QMainWindow):
    SPD = 25

    def __init__(self, bubble):
        super().__init__()

        self.news = fetch_news("video games")
        self.news_index = 0
        self.name = get_response("#getName.capitalize#")
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
        news_label = self.create_label("News", self.open_news)
        news_label.move(0, 50)

        self.labels = [hello_label, quote_label, self.bubble.label, news_label]

        self.WIDTH = QApplication.desktop().screenGeometry().width()
        self.HEIGHT = QApplication.desktop().screenGeometry().height()

        self.setGeometry(0, 0, mwidth, mheight)

        self.move(self.WIDTH // 2, self.HEIGHT // 2)
        self.move_window()

        QTimer.singleShot(5000, self.idle_say)

    def idle_say(self):
        self.open_quotes(None)
        QTimer.singleShot(25_000, self.idle_say)

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

    def open_news(self, _e):
        from voice import say_tts
        title, desc = self.news[self.news_index]
        saying = f"Today's news are {title}...{desc}"
        self.news_index = (self.news_index + 1) % len(self.news)
        self.bubble.change_text(saying)
        self.bubble.move(self.x() - self.bubble.label.width() //
                         2, self.y() - self.bubble.label.height())
        self.bubble.setVisible(True)
        QTimer.singleShot(10000, self.bubble.hide)
        say_tts(saying)

    def open_quotes(self, _e):
        from voice import say_tts
        saying = get_response(f"[name: {self.name}]#origin#")
        self.bubble.change_text(saying)
        self.bubble.move(self.x() - self.bubble.label.width() //
                         2, self.y() - self.bubble.label.height())
        self.bubble.setVisible(True)
        QTimer.singleShot(10000, self.bubble.hide)
        say_tts(saying)

    def show_label(self, _e):
        for lab in self.labels:
            lab.setVisible(not lab.isVisible())

    def toggle_move(self, _e):
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
