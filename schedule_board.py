import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QPushButton, QListWidget


class ScheduleBoard(QWidget):

    def __init__(self, user_data, calendar_date):
        super().__init__()
        self.user_data = user_data
        self.calendar_date = calendar_date

        self.window_title = QLabel(self)

        self.register_btn = QPushButton(self)

        self.calender = QCalendarWidget(self)
        self.schedule_board = QListWidget(self)

        self.set_ui()
        print(self.calendar_date)
        print(type(self.calendar_date))

    def set_ui(self):
        self.setGeometry(350, 300, 600, 480)

        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_combo_box()

        self.set_calender()
        self.set_schedule_board()

    def set_label(self):
        self.window_title.setText('개인별 특이사항')
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 20, 600, 40)

    def set_line(self):
        pass

    def set_btn(self):
        pass

    def set_combo_box(self):
        pass

    def set_calender(self):
        self.calender.setGeometry(150, 80, 300, 200)
        self.calender.setSelectedDate(self.calendar_date)

    def set_schedule_board(self):
        self.schedule_board.setGeometry(50, 300, 500, 150)
