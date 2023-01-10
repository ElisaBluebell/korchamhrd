import time

import pymysql
from time import localtime, strftime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from pyqt5_plugins.examplebuttonplugin import QtGui


class StudentMain(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []
        self.user_curriculum = ''

        self.user_status = QLabel(self)
        self.curriculum_title = QLabel(self)
        self.attend_time = QLabel(self)
        self.cut_off_time = QLabel(self)
        self.comeback_time = QLabel(self)
        self.leave_time = QLabel(self)

        self.log_out_btn = QPushButton(self)
        self.exit_btn = QPushButton(self)

        self.set_label()
        self.set_line()
        self.set_btn()

    def set_db(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT * FROM account_info as a
         INNER JOIN curriculum_db  as b 
         on a.curriculum_id = b.id 
         where a.login_status = 1''')

        self.user_info = list(c.fetchall()[0])
        self.set_user_curriculum()

        c.close()
        conn.close()

    def set_user_curriculum(self):
        self.user_curriculum = self.user_info[11]
        if len(self.user_curriculum) > 12:
            self.curriculum_title.setText(f'{self.user_curriculum[:10]}\n{self.user_curriculum[10:]}')

    def set_label(self):
        self.user_status.setText('입실')
        self.user_status.setFont(QtGui.QFont('D2Coding', 20))
        self.user_status.setGeometry(20, 60, 50, 80)
        self.curriculum_title.setFont(QtGui.QFont('D2Coding', 16))
        self.curriculum_title.setAlignment(Qt.AlignCenter)
        self.curriculum_title.setGeometry(70, 60, 360, 80)

    def set_line(self):
        pass

    def set_btn(self):
        self.log_out_btn.clicked.connect(self.log_out)
        self.exit_btn.clicked.connect(self.quit_program)

    def log_out(self):
        pass

    def quit_program(self):
        self.parent().close()
