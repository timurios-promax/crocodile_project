from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QPushButton, QLabel, \
    QColorDialog, QInputDialog, QStatusBar
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer, QCoreApplication
import sys
import sqlite3
from random import sample
import os


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('playerone.ui', self)
        self.zcopy = self.pix.pixmap().copy()

        self.ask_seem()

        self.ansln.hide()
        self.ansbtn.hide()
        self.ansbtntext.hide()
        self.ansbtnpix.hide()
        self.hintCheck.hide()

        self.restartbtn.hide()
        self.restartbtntext.hide()
        self.restartbtnpix.hide()

        self.exitbtn.hide()
        self.exitbtnpix.hide()
        self.exitbtntext.hide()

        self.image = QImage(681, 431, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.pix.setPixmap(QPixmap(self.image))

        self.start_brush()

        self.count = 1800
        self.start = True
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)

        self.setColorbtn.clicked.connect(self.choose_color)

        self.setSizebtn.clicked.connect(self.choose_size)

        self.nextbtn.clicked.connect(self.next)

        self.ansbtn.clicked.connect(self.checkans)

        self.hintCheck.stateChanged.connect(self.showhint)

        self.restartbtn.clicked.connect(self.restar)

        self.exitbtn.clicked.connect(self.stop)

    def ask_seem(self):
        # создание вариантов выбора темы и слова

        con = sqlite3.connect('krokodile.db')
        cur = con.cursor()

        result = cur.execute("""SELECT seem FROM 'seems'""").fetchall()
        result = list(map(lambda x: x[0], result))

        self.seem = QInputDialog.getItem(self, 'Выбор темы', 'Выберети тему', result)
        sem = cur.execute(f"""SELECT id FROM 'seems' WHERE seem = '{self.seem[0]}'""").fetchall()
        self.seem = self.seem[0]

        result = cur.execute(f"""SELECT word FROM 'words' WHERE seemId = {sem[0][0]}""").fetchall()
        result = sample(result, 3)
        con.close()

        result = list(map(lambda x: x[0], result))
        self.word = QInputDialog.getItem(self, 'Выбор слова', 'Выберети слово', result)
        self.word = self.word[0]

        self.tema.setText(self.tema.text() + self.seem)
        self.slovo.setText(self.slovo.text() + self.word)

    def start_brush(self):
        # стартовые настройки кисти

        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def keyPressEvent(self, event):
        # настройка горячих клавиш

        if int(event.modifiers()) == 67108864:
            if event.key() == Qt.Key_Z:
                self.pix.setPixmap(self.zcopy)
                self.image = self.zcopy.toImage()
            if event.key() == Qt.Key_S:
                self.choose_size()
            if event.key() == Qt.Key_C:
                self.choose_color()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.zcopy = self.pix.pixmap().copy()
            self.drawing = True
            point = QPoint()
            point.setX(event.pos().x() - 10)
            point.setY(event.pos().y() - 50)
            self.lastPoint = point

    def showTime(self):
        # функции таймера

        if self.start:
            self.count -= 1
            if self.count == 0:
                self.start = False
                self.next()

        if self.start:
            text = str(self.count / 10) + " s"
            self.timer.setText(text)

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            point = QPoint()
            point.setX(event.pos().x() - 10)
            point.setY(event.pos().y() - 50)
            painter.drawLine(self.lastPoint, point)
            self.lastPoint = point
            self.pix.setPixmap(QPixmap(self.image))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False


    def choose_color(self):
        self.brushColor = QColorDialog.getColor()

    def choose_size(self):
        self.brushSize = QInputDialog.getInt(
            self, "Выберети цвет", "",
            3, 2, 30, 1)[0]

    def next(self):
        self.tema.hide()
        self.hintstate = True
        self.slovo.hide()
        self.setSizebtn.hide()

        self.nextbtn.hide()
        self.nextbtntext.hide()
        self.nextbtnpix.hide()

        self.timer.hide()
        self.setColorbtn.hide()
        self.ansln.show()
        self.ansbtn.show()
        self.ansbtntext.show()
        self.ansbtnpix.show()
        self.hintCheck.show()

    def checkans(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        if self.ansln.text().lower() == self.word.lower():
            self.statusBar.showMessage('Вы угадали')
            self.statusBar.setStyleSheet('background-color : green')

            self.restartbtn.show()
            self.restartbtntext.show()
            self.restartbtnpix.show()

            self.exitbtn.show()
            self.exitbtnpix.show()
            self.exitbtntext.show()
        else:
            self.statusBar.showMessage('Попробуйте еще')
            self.statusBar.setStyleSheet('background-color : red')

    def showhint(self):
        if self.hintstate:
            self.tema.show()
        else:
            self.tema.hide()
        self.hintstate = not (self.hintstate)

    def restar(self):
        os.system('python "main.py"')
        app.quit()
        self.close()

    def stop(self):
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
