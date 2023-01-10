import sys
import pymysql
import webbrowser

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QApplication
from PyQt5 import QtWidgets, QtGui

from student_main import StudentMain
from teacher_main import TeacherMain


class LoginPage(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []

        self.window_title = QLabel('광주인력개발원', self)
        self.user_id = QLabel('아이디', self)
        self.user_pw = QLabel('비밀번호', self)
        self.header_logo = QLabel(self)

        self.user_id_input = QLineEdit(self)
        self.user_pw_input = QLineEdit(self)

        self.login_btn = QPushButton('로그인', self)
        self.quit_btn = QPushButton('종료', self)
        self.link_btn = QPushButton(self)

        self.set_ui()

    def set_label(self):
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 100, 360, 40)

        self.user_id.setFont(QtGui.QFont('D2Coding', 12))
        self.user_id.setGeometry(20, 180, 50, 20)

        self.user_pw.setFont(QtGui.QFont('D2Coding', 12))
        self.user_pw.setGeometry(20, 240, 65, 20)

    def set_line(self):
        self.user_id_input.setFont(QtGui.QFont('D2Coding', 10))
        self.user_id_input.setGeometry(140, 180, 160, 20)
        self.user_id_input.returnPressed.connect(self.login_process)

        self.user_pw_input.setFont(QtGui.QFont('D2Coding', 10))
        self.user_pw_input.setEchoMode(2)
        self.user_pw_input.setGeometry(140, 240, 160, 20)
        self.user_pw_input.returnPressed.connect(self.login_process)

    def set_btn(self):
        self.login_btn.clicked.connect(self.login_process)
        self.login_btn.setGeometry(100, 300, 60, 30)

        self.quit_btn.clicked.connect(self.quit_program)
        self.quit_btn.setGeometry(200, 300, 60, 30)

        self.link_btn.setIcon(QIcon('image/header_logo.png'))
        self.link_btn.setIconSize(QSize(190, 42))
        self.link_btn.clicked.connect(lambda: webbrowser.open('https://www.hrd.go.kr/hrdp/ma/pmmao/newIndexRenewal.do'))
        self.link_btn.setGeometry(20, 20, 192, 44)

    def set_ui(self):
        self.set_line()
        self.set_label()
        self.set_btn()

    def login_process(self):
        i = 0
        wrong_pw = 0

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('UPDATE korchamhrd.account_info SET `login_status` = 0')
        conn.commit()

        c.execute('SELECT * FROM korchamhrd.account_info;')
        self.user_info = list(c.fetchall())

        c.close()
        conn.close()

        for i in range(len(self.user_info)):
            if self.user_info[i][1] == self.user_id_input.text():
                if self.user_info[i][2] == self.user_pw_input.text():
                    self.user_info = list(self.user_info[i])
                    self.log_in()
                    break

                else:
                    QMessageBox.warning(self, '로그인 실패', '비밀번호를 확인하세요.')
                    self.user_pw_input.cursorPosition()
                    wrong_pw = 1

        i += 1
        if i == len(self.user_info) and type(self.user_info[0]) == tuple and wrong_pw == 0:
            QMessageBox.warning(self, '로그인 실패', '아이디를 확인하세요.')

    def log_in(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute(f'UPDATE korchamhrd.account_info SET `login_status` = 1 WHERE user_id = "{self.user_info[1]}"')
        conn.commit()

        c.close()
        conn.close()

        # AccountInfo DB의 맨 처음엔 6자리의 고유 번호가 있으며 1로 시작할 경우 학생, 2로 시작할 경우 교수를 뜻함.
        if str(self.user_info[0])[:1] == '1':
            student_main.set_db()

            self.user_id_input.clear()
            self.user_pw_input.clear()

            widget.setCurrentIndex(1)

        else:
            self.user_id_input.clear()
            self.user_pw_input.clear()

            widget.setCurrentIndex(2)

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
