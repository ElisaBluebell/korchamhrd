import pymysql
from PyQt5.QtWidgets import *


class StudentMain(QWidget):

    def __init__(self):
        super().__init__()
        self.window_title = QLabel('학생', self)

    def set_label(self):
        self.window_title.setGeometry(40, 40, 160, 220)

    def set_line(self):
        pass

    def set_btn(self):
        pass

    def log_out(self):
        pass

    def quit_program(self):
        pass
