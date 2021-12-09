from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle('8')
    window.setGeometry(0, 0, 1280, 720)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()
