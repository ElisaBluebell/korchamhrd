import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QPushButton, QListWidget, QComboBox


class ScheduleBoard(QWidget):

    def __init__(self, user_data, calendar_date):
        super().__init__()
        self.user_data = user_data
        self.calendar_date = calendar_date

        self.window_title = QLabel(self)
        self.class_selected = QLabel(self)
        self.name_selected = QLabel(self)
        self.date_selected = QLabel(self)

        self.register_btn = QPushButton(self)
        self.close_btn = QPushButton(self)

        self.select_student_name = QComboBox(self)

        self.calender = QCalendarWidget(self)
        self.schedule_board = QListWidget(self)

        self.set_ui()
        print(self.calendar_date)
        print(type(self.calendar_date))
        print(self.user_data)
        print(type(self.user_data[0]))

    def set_label(self):
        self.window_title.setText('개인별 특이사항')
        self.window_title.setFont(QtGui.QFonts('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 20, 600, 40)

        # self.class_selected

        self.name_selected.setText('이름')
        self.name_selected.setGeometry(350, 120, 40, 20)

    def set_line(self):
        pass

    def set_btn(self):
        self.register_btn.setText('등록')
        self.register_btn.setGeometry(350, 260, 60, 20)
        self.register_btn.clicked.connect(self.register_schedule)

        self.close_btn.setText('닫기')
        self.close_btn.setGeometry(490, 260, 60, 20)
        self.close_btn.clicked.connect(self.close_board)

    def set_combo_box(self):
        self.select_student_name.setGeometry(490, 120, 60, 20)

        if self.user_data[0] < 200000:
            self.select_student_name.addItem(self.user_data[3])

        else:
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
            c = conn.cursor()
            
            # id 10만번대는 학생, 20만번대는 교수
            c.execute('SELECT user_name FROM korchamhrd.account_info WHERE id < 200000')
            student = list(c.fetchall())

            for i in range(len(student)):
                self.select_student_name.addItem(student[i][0])

    def set_calender(self):
        self.calender.setGeometry(30, 80, 300, 200)
        self.calender.setSelectedDate(self.calendar_date)

    def set_schedule_board(self):
        self.schedule_board.setGeometry(30, 300, 540, 150)

    def set_ui(self):
        self.setGeometry(350, 300, 600, 480)
        self.setFont(QtGui.QFont('D2Coding'))

        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_combo_box()

        self.set_calender()
        self.set_schedule_board()

    def register_schedule(self):
        pass

    def close_board(self):
        self.close()
