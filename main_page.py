import datetime

import pymysql

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QCalendarWidget, QMessageBox
from PyQt5 import QtGui
from time import strftime

from schedule_board import ScheduleBoard


class MainPage(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []
        self.user_curriculum = ''
        self.schedule_board = 0

        self.user_status = QLabel(self)
        self.curriculum_title = QLabel(self)
        self.attend_time = QLabel(self)
        self.cut_off_time = QLabel(self)
        self.comeback_time = QLabel(self)
        self.leave_time = QLabel(self)
        self.attend_status = QLabel(self)
        self.user_name = QLabel(self)

        self.attend_btn = QPushButton(self)
        self.log_out_btn = QPushButton(self)
        self.close_btn = QPushButton(self)
        self.chat_btn = QPushButton(self)
        self.cut_off_btn = QPushButton(self)

        self.calendar = QCalendarWidget(self)

    def set_db(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 로그인 상태가 참인 DB의 행을 불러옴
        # DB 0=유저 고유번호, 1=이름, 2=메세지수신, 3=결석, 4=지각, 5=조퇴, 6=외출, 8=유저 상태, 9=수업 고유번호
        # 10=입실 시간, 11=외출 시간, 12=퇴실 시간, 13=복귀 시간, 15=남은일수 16=수업명, 17=총 수업일수, 18=반 활성상태
        c.execute(f'''SELECT * FROM korchamhrd.`{str(datetime.date.today())}` as a
         INNER JOIN curriculum_db  as b 
         on a.curriculum_id = b.id 
         where a.login_status = 1''')

        self.user_info = list(c.fetchall()[0])

        c.close()
        conn.close()

        self.set_user_status()
        self.set_user_curriculum()

    def set_label(self):
        self.user_status.setFont(QtGui.QFont('D2Coding', 18))
        self.user_status.setAlignment(Qt.AlignLeft)
        self.user_status.setGeometry(20, 20, 70, 40)

        self.curriculum_title.setFont(QtGui.QFont('D2Coding', 16))
        self.curriculum_title.setAlignment(Qt.AlignRight)
        self.curriculum_title.setGeometry(100, 20, 240, 80)

        self.attend_time.setGeometry(40, 330, 103, 20)
        self.comeback_time.setGeometry(217, 330, 103, 20)
        self.cut_off_time.setGeometry(40, 360, 103, 20)
        self.leave_time.setGeometry(217, 360, 103, 20)

        self.attend_status.setAlignment(Qt.AlignCenter)
        self.attend_status.setGeometry(0, 306, 360, 20)

        self.user_name.setFont(QtGui.QFont('D2Coding', 12))
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setGeometry(30, 77, 300, 20)

    def set_label_text(self):
        self.user_name.setText(f'{self.user_info[1]}님, 환영합니다.')

        if self.user_info[0] < 200000:
            self.attend_time.setText(f'입실 시간 | {self.user_info[10]}')
            self.comeback_time.setText(f'복귀 시간 | {self.user_info[13]}')
            self.cut_off_time.setText(f'외출 시간 | {self.user_info[11]}')
            self.leave_time.setText(f'퇴실 시간 | {self.user_info[12]}')

            self.attend_status.setText(f'출석 {None} 결석 {self.user_info[3]}, 지각 {self.user_info[4]}, '
                                       f'조퇴 {self.user_info[5]}, 외출 {self.user_info[6]}')

        else:
            self.attend_time.setText(f'출근 시간 | {self.user_info[10]}')
            self.comeback_time.setText(f'퇴근 시간 | {self.user_info[12]}')
            self.cut_off_time.setText('')
            self.leave_time.setText('')
            self.attend_status.setText('')

    def set_btn(self):
        self.chat_btn.clicked.connect(self.chat)
        self.chat_btn.setGeometry(220, 400, 80, 40)

        self.log_out_btn.clicked.connect(self.log_out)
        self.log_out_btn.setGeometry(60, 460, 80, 40)

        self.close_btn.clicked.connect(self.quit_program)
        self.close_btn.setGeometry(220, 460, 80, 40)

        self.attend_btn.clicked.connect(self.change_user_status)
        self.cut_off_btn.clicked.connect(self.cut_off)

    def set_btn_text(self):
        self.chat_btn.setText('상담')
        self.log_out_btn.setText('로그아웃')
        self.close_btn.setText('종료')

    def set_btn_activate(self):        # 유저가 출근 or 입실 전일 경우
        if self.user_info[8] == 0:
            self.attend_btn.setGeometry(60, 400, 80, 40)

            if self.user_info[0] < 200000:
                self.attend_btn.setText('입실')

            else:
                self.attend_btn.setText('출근')

        # 유저가 출근 or 입실했을 경우
        elif self.user_info[8] == 1:
            self.attend_btn.setGeometry(60, 400, 80, 40)

            if self.user_info[0] < 200000:
                self.attend_btn.setText('퇴실')

                if self.user_info[13] == 'NULL':
                    self.cut_off_btn.setGeometry(160, 400, 40, 40)
                    self.cut_off_btn.setText('외출')

            else:
                self.attend_btn.setText('퇴근')

        elif self.user_info[8] == 2:
            self.cut_off_btn.setGeometry(160, 400, 40, 40)
            self.cut_off_btn.setText('복귀')

    def set_btn_deactivate(self):
        self.attend_btn.setGeometry(0, 0, 0, 0)
        self.attend_btn.setText('')

        self.cut_off_btn.setGeometry(0, 0, 0, 0)
        self.cut_off_btn.setText('')

    def set_calendar(self):
        self.calendar.setGeometry(30, 100, 300, 200)
        self.set_calendar_background()
        self.calendar.clicked.connect(self.schedule_management)

    def set_calendar_background(self):
        fill_date_background = QTextCharFormat()
        fill_date_background.setBackground(Qt.yellow)
        scheduled_day = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT DISTINCT DATE_FORMAT(the_day, "%Y-%m-%d") FROM korchamhrd.schedule_db 
        WHERE schedule_deleted=0 ORDER BY the_day''')
        temp = list(c.fetchall())

        c.close()
        conn.close()

        for i in range(len(temp)):
            scheduled_day.append(temp[i][0])

        for date in scheduled_day:
            the_day = QDate.fromString(date, "yyyy-MM-dd")
            self.calendar.setDateTextFormat(the_day, fill_date_background)

    def set_ui(self):
        self.set_label()
        self.set_label_text()
        self.set_btn()
        self.set_calendar()
        self.setFont(QtGui.QFont('D2Coding'))

    def schedule_management(self):
        self.schedule_board = ScheduleBoard(self.user_info, self.calendar.selectedDate())
        self.schedule_board.show()

    def set_user_status(self):
        if self.user_info[0] < 200000:
            if self.user_info[8] == 0:
                self.user_status.setText('입실전')
    
            elif self.user_info[8] == 1:
                self.user_status.setText('입실')
    
            elif self.user_info[8] == 2:
                self.user_status.setText('외출')
    
            else:
                self.user_status.setText('퇴실')

        else:
            if self.user_info[8] == 0:
                self.user_status.setText('출근전')
            
            elif self.user_info[8] == 1:
                self.user_status.setText('출근')
                
            else:
                self.user_status.setText('퇴근')
            
    def set_user_curriculum(self):
        self.user_curriculum = self.user_info[16]
        if len(self.user_curriculum) > 14:
            self.curriculum_title.setText(f'{self.user_curriculum[:12]}\n{self.user_curriculum[12:]}')
        else:
            self.curriculum_title.setText(self.user_curriculum)

    def change_user_status(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        if self.user_info[8] == 0:
            self.user_info[8] = 1
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=1, 
            attend_time="{strftime('%I:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            QMessageBox.information(self, '입실', '입실하였습니다.')

        elif self.user_info[8] == 1:
            self.user_info[8] = 3
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=3, 
            leave_time="{strftime('%I:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            # 수업 시간 계산, 요일별 필요충족수업시간에 맞춰 결석 또는 수업

            QMessageBox.information(self, '퇴실', '퇴실하였습니다.')

        c.close()
        conn.close()

        self.set_db()
        self.set_btn_text()
        self.set_btn_deactivate()
        self.set_btn_activate()
        self.set_label_text()
        self.set_user_status()

    def cut_off(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        if self.user_info[8] == 1:
            self.user_info[8] = 2
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=2, 
            cut_time="{strftime('%I:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            QMessageBox.information(self, '외출', '외출하였습니다.')

        elif self.user_info[8] == 2:
            self.user_info[8] = 1
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=1, 
            return_time="{strftime('%I:%M')}", period_cut={self.user_info[6] + 1} WHERE id={self.user_info[0]}''')
            conn.commit()

            QMessageBox.information(self, '복귀', '복귀하였습니다.')

        c.close()
        conn.close()

        self.set_db()
        self.set_btn_text()
        self.set_btn_deactivate()
        self.set_btn_activate()
        self.set_label_text()
        self.set_user_status()

    def chat(self):
        pass

    def do_nothing(self):
        pass

    def log_out(self):
        reply = QMessageBox.question(self, '로그아웃', '로그아웃 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:

            conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
            c = conn.cursor()

            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET login_status=0 
            WHERE id="{self.user_info[0]}"''')
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
