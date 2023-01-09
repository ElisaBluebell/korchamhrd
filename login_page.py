import sys
import pymysql
import webbrowser

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui

from student_main import StudentMain
from teacher_main import TeacherMain


class LoginPage(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []

        self.user_id_input = QLineEdit(self)
        self.user_pw_input = QLineEdit(self)

        self.window_title = QLabel('광주인력개발원', self)
        self.user_id = QLabel('아이디', self)
        self.user_pw = QLabel('비밀번호', self)
        self.header_logo = QLabel(self)

        self.login_btn = QPushButton('로그인', self)
        self.quit_btn = QPushButton('종료', self)
        self.link_btn = QPushButton(self)

        self.set_line()
        self.set_label()
        self.set_btn()

    def set_line(self):
        self.user_id_input.setFont(QtGui.QFont('D2Coding', 10))
        self.user_id_input.setGeometry(140, 180, 160, 20)

        self.user_pw_input.setFont(QtGui.QFont('D2Coding', 10))
        self.user_pw_input.setEchoMode(2)
        self.user_pw_input.setGeometry(140, 240, 160, 20)

    def set_label(self):
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 100, 360, 40)

        self.user_id.setFont(QtGui.QFont('D2Coding', 12))
        self.user_id.setGeometry(20, 180, 50, 20)

        self.user_pw.setFont(QtGui.QFont('D2Coding', 12))
        self.user_pw.setGeometry(20, 240, 65, 20)

        # self.header_logo.setPixmap(QPixmap('image/header_logo.png'))
        # self.header_logo.setGeometry(20, 20, 210, 62)

    def set_btn(self):
        self.login_btn.clicked.connect(self.login_process)
        self.login_btn.setGeometry(100, 300, 60, 30)

        self.quit_btn.clicked.connect(self.quit_program)
        self.quit_btn.setGeometry(200, 300, 60, 30)

        self.link_btn.setIcon(QIcon('image/header_logo.png'))
        self.link_btn.setIconSize(QSize(190, 42))
        self.link_btn.clicked.connect(lambda: webbrowser.open('https://www.hrd.go.kr/hrdp/ma/pmmao/newIndexRenewal.do'))
        self.link_btn.setGeometry(20, 20, 192, 44)

    def login_process(self):
        i = 0
        wrong_pw = 0

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('SELECT * FROM korchamhrd.accountinfo;')
        user_info = list(c.fetchall())

        c.close()
        conn.close()

        for i in range(len(user_info)):
            if user_info[i][1] == self.user_id_input.text():
                if user_info[i][2] == self.user_pw_input.text():
                    user_info = list(user_info[i])
                    print(user_info)
                    break

                else:
                    QMessageBox.warning(self, '로그인 실패', '비밀번호를 확인하세요.')
                    wrong_pw = 1

        i += 1
        if i == len(user_info) and type(user_info[0]) == tuple and wrong_pw == 0:
            QMessageBox.warning(self, '로그인 실패', '아이디를 확인하세요.')

    @staticmethod
    def quit_program():
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    login_page = LoginPage()
    student_main = StudentMain()
    teacher_main = TeacherMain()

    widget.addWidget(login_page)
    widget.addWidget(student_main)
    widget.addWidget(teacher_main)

    widget.setGeometry(0, 0, 360, 540)
    widget.setWindowTitle('고용노동부 HRD-Net')

    widget.show()
    app.exec_()
