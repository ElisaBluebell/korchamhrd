#-*- coding: utf-8 -*-

import datetime
import time

import pymysql
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QListWidget, QPushButton, QWidget, QListWidgetItem


class ChatWindow(QWidget):

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.chat_db = []
        self.chat_db_name = ''

        self.title = QLabel(self)
        self.opponent_class = QLabel(self)
        self.opponent_name = QLabel(self)

        self.chat_input = QLineEdit(self)

        self.go_back_btn = QPushButton(self)
        self.send_chat_btn = QPushButton(self)

        self.select_opponent_class = QComboBox(self)
        self.select_opponent_name = QComboBox(self)

        self.chat_list = QListWidget(self)

        self.set_ui()
        self.set_db()

        self.refresh_ui()
        refresh_chat = threading.Thread(target=self.refresh_chat, daemon=True)
        refresh_chat.start()

    def set_label(self):
        self.title.setText('일대일 상담')
        self.title.setFont(QFont('D2Coding', 20))
        self.title.setGeometry(0, 20, 360, 30)
        self.title.setAlignment(Qt.AlignCenter)

        self.opponent_name.setText('이름')
        self.opponent_name.setGeometry(20, 100, 60, 20)

    def set_line(self):
        self.chat_input.setGeometry(20, 460, 260, 20)
        self.chat_input.returnPressed.connect(self.send_message)
        self.chat_input.setMaxLength(15)

    def set_btn(self):
        self.send_chat_btn.clicked.connect(self.send_message)
        self.send_chat_btn.setGeometry(300, 460, 40, 20)
        self.send_chat_btn.setText('보내기')

        self.go_back_btn.clicked.connect(self.close_window)
        self.go_back_btn.setGeometry(20, 500, 320, 20)
        self.go_back_btn.setText('나가기')

    def set_list_widget(self):
        self.chat_list.setGeometry(20, 140, 320, 300)

    def set_combo_box(self):
        self.select_opponent_name.setGeometry(100, 100, 240, 20)

    def activate_ui(self):
        temp = []
        new_chat_member = []
        new_chat_class = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 학생일 경우
        if self.user_info[0] < 200000:

            c.execute(f'SHOW TABLES LIKE "%{self.user_info[1]}%"')
            chat_table = c.fetchall()
            for i in range(len(chat_table)):
                c.execute(
                    f'SELECT COUNT(student_alarm) FROM korchamhrd.`{chat_table[i][0]}` WHERE student_alarm=1')
                if c.fetchone()[0] != 0:
                    new_chat_member.append(chat_table[i][0][:3])

            for i in range(len(self.chat_db)):
                # 교수에 한해 이름을 체크박스에 추가함
                if self.chat_db[i][2] == '교수':
                    if self.chat_db[i][1] in new_chat_member:
                        self.select_opponent_name.addItem(self.chat_db[i][1] + '*')
                    else:
                        self.select_opponent_name.addItem(self.chat_db[i][1])

        else:
            # 수강과정 체크박스와 라벨 표시
            self.opponent_class.setText('수강과정')
            self.opponent_class.setGeometry(20, 60, 60, 20)
            self.select_opponent_class.setGeometry(100, 60, 240, 20)

            c.execute(f'SHOW TABLES LIKE "%{self.user_info[1]}%"')
            chat_table = c.fetchall()
            for i in range(len(chat_table)):
                c.execute(
                    f'SELECT COUNT(teacher_alarm) FROM korchamhrd.`{chat_table[i][0]}` WHERE teacher_alarm=1')
                if c.fetchone()[0] != 0:
                    new_chat_member.append(chat_table[i][0][4:])

            for i in range(len(new_chat_member)):
                c.execute(f'SELECT DISTINCT b.class_name FROM korchamhrd.`{str(datetime.date.today())}` AS a INNER JOIN korchamhrd.curriculum_db AS b ON a.curriculum_id=b.id WHERE a.user_name="{new_chat_member[i]}"')
                new_chat_class.append(c.fetchone()[0])

            # 수강과정명이 중복되지 않게 체크박스에 추가함
            for i in range(len(self.chat_db)):
                if self.chat_db[i][2] not in temp and self.chat_db[i][3] == 1:
                    temp.append(self.chat_db[i][2])
                    if self.chat_db[i][2] not in new_chat_class:
                        self.select_opponent_class.addItem(self.chat_db[i][2])
                    else:
                        self.select_opponent_class.addItem(self.chat_db[i][2] + '*')

            # 수강과정명에 따라 체크박스에 이름을 넣는 함수 호출
            self.select_opponent_class.currentTextChanged.connect(self.change_selected_name)

        # 대상명이 변경될 시 채팅창 호출
        self.select_opponent_name.currentTextChanged.connect(self.open_chat)

    def deactivate_ui(self):
        self.opponent_class.setText('')
        self.opponent_class.setGeometry(0, 0, 0, 0)

        self.select_opponent_name.clear()

        self.select_opponent_class.clear()
        self.select_opponent_class.setGeometry(0, 0, 0, 0)

    def change_selected_name(self):
        self.select_opponent_name.clear()

        new_chat_member = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute(f'SHOW TABLES LIKE "%{self.user_info[1]}%"')
        chat_table = c.fetchall()
        for i in range(len(chat_table)):
            c.execute(
                f'SELECT COUNT(teacher_alarm) FROM korchamhrd.`{chat_table[i][0]}` WHERE teacher_alarm=1')
            if c.fetchone()[0] != 0:
                new_chat_member.append(chat_table[i][0][4:])

        for i in range(len(self.chat_db)):
            if '*' in self.select_opponent_class.currentText():
                length = len(self.select_opponent_class.currentText()) - 1
                class_name = self.select_opponent_class.currentText()[:length]

            else:
                class_name = self.select_opponent_class.currentText()

            # 대상의 수강과정이 체크박스에 선택된 과정과 같을 경우 체크박스에 추가함
            if self.chat_db[i][2] == class_name:
                if self.chat_db[i][1] in new_chat_member:
                    self.select_opponent_name.addItem(self.chat_db[i][1] + '*')
                else:
                    self.select_opponent_name.addItem(self.chat_db[i][1])

    def set_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT a.id, a.user_name, b.class_name, b.class_status FROM korchamhrd.account_info AS a 
        INNER JOIN korchamhrd.curriculum_db AS b ON a.curriculum_id=b.id ORDER BY a.user_name''')
        self.chat_db = list(c.fetchall())

        c.close()
        conn.close()

    # 쓰레드로 돌릴 채팅창 최신화
    def refresh_chat(self):
        while True:
            self.read_message()
            time.sleep(0.5)

    def refresh_ui(self):
        self.deactivate_ui()
        self.activate_ui()

    def set_ui(self):
        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_list_widget()
        self.set_combo_box()
        self.refresh_ui()

        self.setFont(QFont('D2Coding'))
        self.setGeometry(420, 120, 360, 540)
        self.setWindowIcon(QIcon('image/logo.png'))
        self.setWindowTitle('상담')

    def open_chat(self):
        self.create_chat()
        self.read_message()

    # 채팅창이 없을 경우 교수명_학생명으로 채팅 테이블 작성
    def create_chat(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()
        if self.user_info[0] < 200000:
            if '*' in self.select_opponent_name.currentText():
                length = len(self.select_opponent_name.currentText()) - 1
                self.chat_db_name = self.select_opponent_name.currentText()[:length] + '_' + self.user_info[1]
            else:
                self.chat_db_name = self.select_opponent_name.currentText() + '_' + self.user_info[1]
            # 보낸이, 내용, 시간, 학생알림, 교수알림 값을 가짐
            c.execute(f'CREATE TABLE IF NOT EXISTS korchamhrd.`{self.chat_db_name}` (sender TEXT NOT NULL, '
                      f'content TEXT NOT NULL, time TEXT NOT NULL, student_alarm INT NOT NULL, '
                      f'teacher_alarm INT NOT NULL)')

        else:
            if '*' in self.select_opponent_name.currentText():
                length = len(self.select_opponent_name.currentText()) - 1
                self.chat_db_name = self.user_info[1] + '_' + self.select_opponent_name.currentText()[:length]
            else:
                self.chat_db_name = self.user_info[1] + '_' + self.select_opponent_name.currentText()
            c.execute(f'CREATE TABLE IF NOT EXISTS korchamhrd.`{self.chat_db_name}` (sender TEXT NOT NULL, '
                      f'content TEXT NOT NULL, time TEXT NOT NULL, student_alarm INT NOT NULL, '
                      f'teacher_alarm INT NOT NULL)')

        c.close()
        conn.close()

    def send_message(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute(f'INSERT INTO korchamhrd.{self.chat_db_name} VALUES ("{self.user_info[1]}", '
                  f'"{self.chat_input.text()}", "{datetime.datetime.now()}", 1, 1)')
        conn.commit()

        c.close()
        conn.commit()

        self.chat_input.clear()
        self.read_message()

    def read_message(self):
        self.chat_list.clear()
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        if self.user_info[0] < 200000:
            c.execute(f'UPDATE korchamhrd.{self.chat_db_name} SET student_alarm=0')
            conn.commit()

        else:
            c.execute(f'UPDATE korchamhrd.{self.chat_db_name} SET teacher_alarm=0')
            conn.commit()

        # 가장 최신 채팅 17개를 가져옴
        c.execute(f'SELECT * FROM (SELECT * FROM korchamhrd.{self.chat_db_name} ORDER BY `time` DESC LIMIT 17) '
                  f'A ORDER BY `time` ASC')
        chat_content = c.fetchall()

        # [시간] 발신자: 내용 의 형식으로 삽입
        for i in range(len(chat_content)):
            self.chat_list.addItem(QListWidgetItem(f'[{chat_content[i][2][5:16]}] {chat_content[i][0]}: '
                                                   f'{chat_content[i][1]}'))

        c.close()
        conn.close()

    def close_window(self):
        self.deactivate_ui()
        self.close()
