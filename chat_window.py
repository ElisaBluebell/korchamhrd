from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox


class ChatWindow(QWidget):

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

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
        self.select_opponent_name.setGeometry(80, 100, 240, 20)

    def activate_ui(self):
        self.opponent_class.setText('수강과정')
        self.opponent_class.setGeometry(20, 60, 60, 20)

        self.select_opponent_class.setGeometry(80, 60, 240, 20)

    def deactivate_ui(self):
        self.opponent_class.setText('')
        self.opponent_class.setGeometry(0, 0, 0, 0)

        self.select_opponent_class.clear()
        self.select_opponent_class.setGeometry(0, 0, 0, 0)

    def set_db(self):
        pass

    def set_ui(self):
        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_list_widget()
        self.set_combo_box()

        self.setFont(QFont('D2Coding'))
        self.setGeometry(420, 120, 360, 540)
        self.setWindowIcon(QIcon('image/logo.png'))
        self.setWindowTitle('상담')

    def send_message(self):
        pass

    def close_window(self):
        self.close()
