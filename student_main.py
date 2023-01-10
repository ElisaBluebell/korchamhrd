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
        self.user_status = ''
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

        c.close()
        conn.close()

        self.set_user_status()
        self.set_user_curriculum()

    def set_user_status(self):
        self.user_status.setText('입실')

    def set_user_curriculum(self):
        self.user_curriculum = self.user_info[12]
        if len(self.user_curriculum) > 12:
            self.curriculum_title.setText(f'{self.user_curriculum[:10]}\n{self.user_curriculum[10:]}')

    def set_label(self):
        self.user_status.setFont(QtGui.QFont('D2Coding', 20))
        self.user_status.setGeometry(20, 60, 50, 80)

        self.curriculum_title.setFont(QtGui.QFont('D2Coding', 16))
        self.curriculum_title.setAlignment(Qt.AlignCenter)
        self.curriculum_title.setGeometry(70, 60, 360, 80)

        self.attend_time.setFont(QtGui.QFont('D2Coding'))
        self.attend_time.setText(f'입실 시간 | 32:43')
        self.attend_time.setGeometry(40, 350, 103, 20)

        self.comeback_time.setFont(QtGui.QFont('D2Coding'))
        self.comeback_time.setText(f'복귀 시간 | 12:40')
        self.comeback_time.setGeometry(217, 350, 103, 20)

        self.cut_off_time.setFont(QtGui.QFont('D2Coding'))
        self.cut_off_time.setText(f'외출 시간 | 12:40')
        self.cut_off_time.setGeometry(40, 380, 103, 20)

        self.leave_time.setFont(QtGui.QFont('D2Coding'))
        self.leave_time.setText(f'퇴실 시간 | 12:40')
        self.leave_time.setGeometry(217, 380, 103, 20)

    def set_line(self):
        pass

    def set_btn(self):
        self.log_out_btn.clicked.connect(self.log_out)
        self.log_out_btn.setGeometry(80, 460, 60, 40)
        self.log_out_btn.setText('로그아웃')

        self.exit_btn.clicked.connect(self.quit_program)
        self.exit_btn.setGeometry(220, 460, 60, 40)
        self.exit_btn.setText('종료')

    def read_user_status(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.close()
        conn.close()

    def log_out(self):
        reply = QMessageBox.question(self, '로그아웃', '로그아웃 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:

            conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
            c = conn.cursor()

            c.execute(f'UPDATE korchamhrd.account_info SET login_status=0 WHERE user_id="{self.user_info[1]}"')
            conn.commit()

            c.close()
            conn.close()

            self.parent().setCurrentIndex(0)

        else:
            pass

    def quit_program(self):
        reply = QMessageBox.question(self, '프로그램 종료', '프로그램을 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent().close()

        else:
            pass
