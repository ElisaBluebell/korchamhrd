import pymysql

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QListWidget, QPushButton, QWidget, QListWidgetItem


class ChatWindow(QWidget):

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.chat_db = []

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

    def set_label(self):
        self.title.setText('일대일 상담')
        self.title.setFont(QFont('D2Coding', 20))
        self.title.setGeometry(0, 20, 360, 30)
        self.title.setAlignment(Qt.AlignCenter)

        self.opponent_name.setText('이름')
        self.opponent_name.setGeometry(20, 100, 60, 20)

    def set_line(self):
        self.chat_input.setGeometry(20, 460, 260, 20)

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
        # 학생일 경우
        if self.user_info[0] < 200000:
            for i in range(len(self.chat_db)):
                if self.chat_db[i][2] == '교수':
                    self.select_opponent_name.addItem(self.chat_db[i][1])
        else:
            self.opponent_class.setText('수강과정')
            self.opponent_class.setGeometry(20, 60, 60, 20)

            self.select_opponent_class.setGeometry(100, 60, 240, 20)
            for i in range(len(self.chat_db)):
                print(1)
                if self.chat_db[i][2] not in temp and self.chat_db[i][3] == 1:
                    print(2)
                    temp.append(self.chat_db[i][2])
                    print(3)
                    self.select_opponent_class.addItem(self.chat_db[i][2])
                    print(4)
            self.select_opponent_class.currentTextChanged.connect(self.change_selected_name)

            self.change_selected_name()
        self.select_opponent_name.currentTextChanged.connect(self.open_chat)

    def deactivate_ui(self):
        self.opponent_class.setText('')
        self.opponent_class.setGeometry(0, 0, 0, 0)

        self.select_opponent_name.clear()

        self.select_opponent_class.clear()
        self.select_opponent_class.setGeometry(0, 0, 0, 0)

    def change_selected_name(self):
        self.select_opponent_name.clear()
        for i in range(len(self.chat_db)):
            if self.chat_db[i][2] == self.select_opponent_class.currentText():
                self.select_opponent_name.addItem(self.chat_db[i][1])

    def set_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT a.id, a.user_name, b.class_name, b.class_status FROM korchamhrd.account_info AS a 
        INNER JOIN korchamhrd.curriculum_db AS b ON a.curriculum_id=b.id ORDER BY b.id''')
        self.chat_db = list(c.fetchall())

        c.close()
        conn.close()

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
        # 학생
        # if self.user_info < 200000:

    def create_chat(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        if self.user_info[0] < 200000:
            c.execute(f'CREATE TABLE IF NOT EXISTS korchamhrd.`{self.select_opponent_name.currentText()}_'
                      f'{self.user_info[1]}` (sender TEXT NOT NULL, content TEXT NOT NULL, time TEXT NOT NULL, '
                      f'alarm INT NOT NULL)')

        else:
            if self.select_opponent_name.currentText() and self.select_opponent_name.currentText() != self.user_info[1]:
                c.execute(f'CREATE TABLE IF NOT EXISTS korchamhrd.`{self.user_info[1]}_'
                          f'{self.select_opponent_name.currentText()}` (sender TEXT NOT NULL, content TEXT NOT NULL, '
                          f'time TEXT NOT NULL, alarm INT NOT NULL)')

            else:
                pass

    def send_message(self):
        self.read_message()

    def read_message(self):
        self.chat_list.addItem(QListWidgetItem('a'))

    def close_window(self):
        self.close()
