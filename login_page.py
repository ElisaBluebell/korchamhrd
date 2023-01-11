import sys
import pymysql
import webbrowser

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QApplication
from PyQt5 import QtWidgets, QtGui

from main_page import MainPage


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
        self.close_btn = QPushButton('종료', self)
        self.link_btn = QPushButton(self)

        self.set_ui()

    def set_label(self):
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 100, 360, 40)

        self.user_id.setGeometry(20, 180, 50, 20)

        self.user_pw.setGeometry(20, 240, 65, 20)

    def set_line(self):
        self.user_id_input.setGeometry(140, 180, 160, 20)
        self.user_id_input.returnPressed.connect(self.login_process_from_id_input)

        self.user_pw_input.setEchoMode(2)
        self.user_pw_input.setGeometry(140, 240, 160, 20)
        self.user_pw_input.returnPressed.connect(self.login_process)

    def set_btn(self):
        self.login_btn.clicked.connect(self.login_process_with_btn)
        self.login_btn.setGeometry(100, 300, 60, 30)

        self.close_btn.clicked.connect(self.quit_program)
        self.close_btn.setGeometry(200, 300, 60, 30)

        self.link_btn.setIcon(QIcon('image/header_logo.png'))
        self.link_btn.setIconSize(QSize(190, 42))
        self.link_btn.clicked.connect(self.open_web_browser)
        self.link_btn.setGeometry(20, 20, 192, 44)

    def set_ui(self):
        self.set_line()
        self.set_label()
        self.set_btn()
        self.setFont(QtGui.QFont('D2Coding'))

    # 아이디 입력 라인에딧을 통해 로그인할 경우 커서를 정상 위치에 옮겨두기 위해 비밀번호 입력 라인에딧으로 커서를 보냄
    def login_process_from_id_input(self):
        self.focusNextChild()
        self.login_process()

    # 로그인 버튼을 통해 로그인할 경우
    def login_process_with_btn(self):
        self.focusPreviousChild()
        self.login_process()

    def login_process(self):
        # 비밀번호가 틀렸을 때 ID 확인과 메세지 중복출력 방지를 위해 비밀번호 일치 여부 변수 선언 및 초기화
        wrong_pw = 0

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 로그인 상태 1 = 로그인, 0 = 로그아웃 상태, 상태 초기화
        c.execute('UPDATE korchamhrd.account_info SET `login_status` = 0')
        conn.commit()

        c.execute('''SELECT a.id, a.user_id, a.user_pw 
        FROM korchamhrd.account_info AS a 
        INNER JOIN korchamhrd.curriculum_db AS b 
        ON a.curriculum_id = b.id 
        WHERE b.class_status = 1;''')
        self.user_info = list(c.fetchall())

        c.close()
        conn.close()

        for i in range(len(self.user_info)):
            # user_id와 user_pw가 일치하는 값이 있을 경우 로그인 함수 실행
            if self.user_info[i][1] == self.user_id_input.text():
                if self.user_info[i][2] == self.user_pw_input.text():
                    self.user_info = list(self.user_info[i])
                    # 로그인 이후 로그아웃 했을 때 커서를 아이디 창으로 보내기 위해 포커스를 앞으로 올림
                    self.focusPreviousChild()
                    self.log_in()
                    break

                else:
                    QMessageBox.warning(self, '로그인 실패', '비밀번호를 확인하세요.')
                    self.user_pw_input.cursorPosition()
                    wrong_pw = 1
                    # 자동 비밀번호 전체선택
                    self.focusPreviousChild()
                    self.focusNextChild()

        if type(self.user_info[0]) == tuple and wrong_pw == 0:
            QMessageBox.warning(self, '로그인 실패', '아이디를 확인하세요.')
            self.focusPreviousChild()

    def log_in(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute(f'UPDATE korchamhrd.account_info SET `login_status` = 1 WHERE id = "{self.user_info[0]}"')
        conn.commit()

        c.close()
        conn.close()

        # 현재 불러온 db를 토대로 메인 페이지의 db 세팅
        main_page.set_db()

        self.user_id_input.clear()
        self.user_pw_input.clear()

        widget.setCurrentIndex(1)

    @staticmethod
    def open_web_browser():
        webbrowser.open('https://www.hrd.go.kr/hrdp/ma/pmmao/newIndexRenewal.do')

    def quit_program(self):
        reply = QMessageBox.question(self, '프로그램 종료', '프로그램을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    login_page = LoginPage()
    main_page = MainPage()

    widget.addWidget(login_page)
    widget.addWidget(main_page)

    widget.setGeometry(0, 0, 360, 540)
    widget.setWindowTitle('고용노동부 HRD-Net')

    widget.show()
    app.exec_()
