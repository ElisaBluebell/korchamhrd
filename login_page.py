import datetime
import pymysql
import sys
import webbrowser

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget

from main_page import MainPage


class LoginPage(QWidget):

    def __init__(self):
        super().__init__()
        # 유저 DB를 담을 리스트
        self.user_info = []
        # 첫 로그인 확인을 위한 변수
        self.log_in_count = 0

        # ui 설정
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
        # 출석부 제작 함수
        self.set_attendance()

    # 부르면 켜지등가
    @staticmethod
    def set_attendance():
        # DB 임시저장용 변수
        temp = ''
        # 커서 세팅
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 일단 읽어오고
        try:
            c.execute(f'SELECT * FROM korchamhrd.`{str(datetime.date.today())}`')
            temp = c.fetchall()
        except:
            pass

        # 테이블이 만들어져있지 않을 경우 <오늘>을 이름으로 하는 출석부 테이블을 작성함
        # 기존에 작성했던 user_account 테이블에서 로그인에만 필요한 id와 pw를 제외하고 만들어줌
        c.execute(f'''CREATE TABLE IF NOT EXISTS korchamhrd.`{str(datetime.date.today())}` (id INT NOT NULL, 
        user_name TEXT NOT NULL, message_reception INT NOT NULL, absence INT NOT NULL, tardy INT NOT NULL, 
        leave_early INT NOT NULL, period_cut INT NOT NULL, login_status INT NOT NULL, user_status INT NOT NULL, 
        curriculum_id INT NOT NULL, attend_time TEXT, cut_time TEXT, leave_time TEXT, return_time TEXT, 
        day_left INT NOT NULL, PRIMARY KEY (id))''')

        # 오늘자 테이블이 이미 있을 경우 pass
        if temp:
            pass
        else:
            # 오늘자 테이블이 없을 경우 이전 출석부에서 내용을 긁어와서
            c.execute(f'''SELECT * FROM korchamhrd.`{str(datetime.date.today() - datetime.timedelta(1))}`''')
            temp = list(c.fetchall())
            # 변동사항을 적용하여 새로운 테이블에 삽입함
            for i in range(len(temp)):
                c.execute(f'''INSERT INTO korchamhrd.`{str(datetime.date.today())}` VALUES ({temp[i][0]}, 
                "{temp[i][1]}", {temp[i][2]}, {temp[i][3]}, {temp[i][4]}, {temp[i][5]}, {temp[i][6]}, 0, 
                0, {temp[i][9]}, "NULL", "NULL", "NULL", "NULL", {temp[i][14] - 1})''')
                conn.commit()

        c.close()
        conn.close()

    # 라벨 스타일 세팅
    def set_label(self):
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 100, 360, 40)

        self.user_id.setGeometry(20, 180, 50, 20)

        self.user_pw.setGeometry(20, 240, 65, 20)

    # 라인 스타일 및 스위치 세팅
    def set_line(self):
        self.user_id_input.setGeometry(140, 180, 160, 20)
        self.user_id_input.returnPressed.connect(self.login_process_from_id_input)

        self.user_pw_input.setEchoMode(2)
        self.user_pw_input.setGeometry(140, 240, 160, 20)
        self.user_pw_input.returnPressed.connect(self.login_process)

    # 버튼 스타일 및 스위치 세팅
    def set_btn(self):
        self.login_btn.clicked.connect(self.login_process_with_btn)
        self.login_btn.setGeometry(100, 300, 60, 30)

        self.close_btn.clicked.connect(self.quit_program)
        self.close_btn.setGeometry(200, 300, 60, 30)

        self.link_btn.setIcon(QIcon('image/header_logo.png'))
        self.link_btn.setIconSize(QSize(190, 42))
        self.link_btn.clicked.connect(self.open_web_browser)
        self.link_btn.setGeometry(20, 20, 192, 44)

    # 창 기본 세팅
    def set_ui(self):
        self.setWindowIcon(QIcon('image/logo.png'))

        self.set_line()
        self.set_label()
        self.set_btn()
        self.setFont(QtGui.QFont('D2Coding'))

    # 아이디 입력 라인에딧을 통해 로그인할 경우 커서를 기준점인 비밀번호 입력 라인에딧으로 커서를 보냄
    def login_process_from_id_input(self):
        # 다음 항목(비밀번호 라인에딧)으로 커서를 보낸 후
        self.focusNextChild()
        # 로그인 로직 실행
        self.login_process()

    # 로그인 버튼을 통해 로그인할 경우
    def login_process_with_btn(self):
        # 이전 항목(비밀번호 라인에딧)으로 커서를 보냄
        self.focusPreviousChild()
        self.login_process()

    def login_process(self):
        # 비밀번호가 틀렸을 때 ID 확인과 메세지 중복출력 방지를 위해 비밀번호 일치 여부 변수 선언 및 초기화
        wrong_pw = 0

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 로그인 상태 1 = 로그인, 0 = 로그아웃 상태, 상태 초기화
        c.execute(f'UPDATE korchamhrd.`{str(datetime.date.today())}` SET `login_status` = 0')
        conn.commit()

        # 0=유저 고유번호, 1=유저 계정 id, 2=유저 계정 비밀번호, 현재 반이 활성화 된 상태에 한해서 데이터를 불러옴
        c.execute('''SELECT a.id, a.user_id, a.user_pw 
        FROM korchamhrd.account_info AS a 
        INNER JOIN korchamhrd.curriculum_db AS b 
        ON a.curriculum_id=b.id 
        WHERE b.class_status=1;''')
        self.user_info = list(c.fetchall())

        c.close()
        conn.close()

        # id, pw 일치여부 판별을 위한 반복문
        for i in range(len(self.user_info)):
            # user_id가 DB상의 id와 일치하는 경우
            if self.user_info[i][1] == self.user_id_input.text():
                # 비밀번호 일치 여부 판별, 비밀번호도 일치할 경우
                if self.user_info[i][2] == self.user_pw_input.text():
                    # 유저 정보를 일치하는 정보로 치환한 후
                    self.user_info = list(self.user_info[i])
                    # 로그인 이후 로그아웃 했을 때 커서를 현 기준점인 pw에서 id로 보내기 위해 포커스를 앞으로 올림
                    self.focusPreviousChild()
                    self.log_in()
                    # 작업 멈춤
                    break

                # id만 일치하는 경우 비밀번호 틀림 판정
                else:
                    QMessageBox.warning(self, '로그인 실패', '비밀번호를 확인하세요.')
                    self.user_pw_input.cursorPosition()
                    # 비밀번호 틀림 변수를 참으로 바꿔주고
                    wrong_pw = 1
                    # 비밀번호 틀릴 시 자동으로 비밀번호가 전체선택되게 한 번 흔들어줌
                    self.focusPreviousChild()
                    self.focusNextChild()
                    break

        # 유저 정보 0번째 값이 튜플(기본형)이고(치환되지 않았고) 비밀번호 틀림 변수가 거짓일 경우 아이디 틀림 판정
        if type(self.user_info[0]) == tuple and wrong_pw == 0:
            QMessageBox.warning(self, '로그인 실패', '아이디를 확인하세요.')
            # 아이디가 틀렸으니 커스를 기준점에서 한 칸 올려 아이디 칸 전체선택
            self.focusPreviousChild()

    def log_in(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 로그인 한 아이디의 출석부 상 로그인 여부를 참으로 바꿔줌
        c.execute(f'UPDATE korchamhrd.`{str(datetime.date.today())}` SET `login_status` = 1 '
                  f'WHERE id = "{self.user_info[0]}"')
        conn.commit()

        c.close()
        conn.close()

        # 현재 불러온 db를 토대로 메인 페이지의 db 세팅
        main_page.set_db()

        # 이전에 로그인을 실행한 적이 없을 경우
        if self.log_in_count == 0:
            # 메인 페이지 ui를 깔아주고
            main_page.set_ui()
            # 로그인 실행 여부를 참으로 바꿔줌
            self.log_in_count = 1

        # 버튼의 텍스트 설정 및
        main_page.set_btn_text()
        # 초기화 개념의 반응형 버튼 무력화
        main_page.set_btn_deactivate()

        # 토요일, 일요일에는 로그인 버튼, 외출 버튼이 활성화되지 않음, 그 외 요일에는 버튼 활성화
        if datetime.datetime.today().weekday() != 5 and datetime.datetime.today().weekday() != 6:
            main_page.set_btn_activate()

        # 라벨 텍스트와 유저 상태를 현재 로그인 하는 유저에 맞게 설정
        main_page.set_label_text()
        main_page.set_user_status()

        # 로그인 창의 id pw 입력 라인 초기화
        self.user_id_input.clear()
        self.user_pw_input.clear()

        # 로그인 스택으로 이동
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
