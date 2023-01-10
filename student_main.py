import pymysql

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QCalendarWidget, QMessageBox
from PyQt5 import QtGui

from schedule_board import ScheduleBoard


class StudentMain(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []
        self.user_status_chk = ''
        self.user_curriculum = ''
        self.cut_off_btn = ''

        self.user_status = QLabel(self)
        self.curriculum_title = QLabel(self)
        self.attend_time = QLabel(self)
        self.cut_off_time = QLabel(self)
        self.comeback_time = QLabel(self)
        self.leave_time = QLabel(self)

        self.attend_btn = QPushButton(self)
        self.log_out_btn = QPushButton(self)
        self.close_btn = QPushButton(self)
        self.chat_btn = QPushButton(self)

        self.calender = QCalendarWidget(self)
        self.schedule_board = 0

        self.set_ui()

    def set_db(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT * FROM account_info as a
         INNER JOIN curriculum_db  as b 
         on a.curriculum_id = b.id 
         where a.login_status = 1''')

        self.user_info = list(c.fetchall()[0])
        self.user_status_chk = self.user_info[9]

        c.close()
        conn.close()

        self.set_user_status()
        self.set_user_curriculum()

    def set_label(self):
        self.user_status.setFont(QtGui.QFont('D2Coding', 20))
        self.user_status.setAlignment(Qt.AlignCenter)
        self.user_status.setGeometry(40, 10, 50, 80)

        self.curriculum_title.setFont(QtGui.QFont('D2Coding', 16))
        self.curriculum_title.setAlignment(Qt.AlignCenter)
        self.curriculum_title.setGeometry(90, 10, 270, 80)

        self.attend_time.setFont(QtGui.QFont('D2Coding'))
        self.attend_time.setText(f'입실 시간 | 32:43')
        self.attend_time.setGeometry(40, 330, 103, 20)

        self.comeback_time.setFont(QtGui.QFont('D2Coding'))
        self.comeback_time.setText(f'복귀 시간 | 12:40')
        self.comeback_time.setGeometry(217, 330, 103, 20)

        self.cut_off_time.setFont(QtGui.QFont('D2Coding'))
        self.cut_off_time.setText(f'외출 시간 | 12:40')
        self.cut_off_time.setGeometry(40, 360, 103, 20)

        self.leave_time.setFont(QtGui.QFont('D2Coding'))
        self.leave_time.setText(f'퇴실 시간 | 12:40')
        self.leave_time.setGeometry(217, 360, 103, 20)

    def set_line(self):
        pass

    def set_btn(self):
        self.attend_btn.clicked.connect(self.change_user_status)
        self.attend_btn.setGeometry(60, 400, 80, 40)
        self.attend_btn.setText('입실')

        self.chat_btn.clicked.connect(self.chat)
        self.chat_btn.setGeometry(220, 400, 80, 40)
        self.chat_btn.setText('상담')

        self.log_out_btn.clicked.connect(self.log_out)
        self.log_out_btn.setGeometry(60, 460, 80, 40)
        self.log_out_btn.setText('로그아웃')

        self.close_btn.clicked.connect(self.quit_program)
        self.close_btn.setGeometry(220, 460, 80, 40)
        self.close_btn.setText('종료')

    def set_calender(self):
        self.calender.setGeometry(30, 100, 300, 200)
        self.calender.clicked.connect(self.schedule_management)

    def set_ui(self):
        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_calender()

    def schedule_management(self):
        self.schedule_board = ScheduleBoard(self.user_info, self.calender.selectedDate())
        self.schedule_board.show()

    def set_user_status(self):
        if self.user_status_chk == 0:
            self.user_status.setText('대기')

        elif self.user_status_chk == 1:
            self.user_status.setText('입실')

        elif self.user_status_chk == 2:
            self.user_status.setText('외출')

        else:
            self.user_status.setText('퇴실')

    def set_user_curriculum(self):
        self.user_curriculum = self.user_info[12]
        if len(self.user_curriculum) > 14:
            self.curriculum_title.setText(f'{self.user_curriculum[:12]}\n{self.user_curriculum[12:]}')

    @staticmethod
    def change_user_status():
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.close()
        conn.close()

    def chat(self):
        pass

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
        reply = QMessageBox.question(self, '프로그램 종료', '프로그램을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent().close()

        else:
            pass
