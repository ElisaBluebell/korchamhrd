#-*- coding: utf-8 -*-

import datetime
import threading

import pymysql
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import QCalendarWidget, QLabel, QMessageBox, QPushButton, QWidget
from time import strftime

from schedule_board import ScheduleBoard
from chat_window import ChatWindow


class MainPage(QWidget):

    def __init__(self):
        super().__init__()
        self.user_info = []
        self.schedule_board = 0
        self.chat_window = 0

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
        th1 = threading.Thread(target=self.refresh_calendar, daemon=True)
        th1.start()
        chat_alarm = threading.Thread(target=self.chat_alarm, daemon=True)
        chat_alarm.start()

    def set_db(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 로그인 상태가 참인 DB의 행을 불러옴
        # DB 0=유저 고유번호, 1=이름, 2=메세지수신, 3=결석, 4=지각, 5=조퇴, 6=외출, 8=유저 상태, 9=수업 고유번호
        # 10=입실 시간, 11=외출 시간, 12=퇴실 시간, 13=복귀 시간, 14=남은일수, 17=수업명, 18=총 수업일수, 19=반 활성상태
        c.execute(f'''SELECT * FROM korchamhrd.`{str(datetime.date.today())}` as a
         INNER JOIN curriculum_db  as b 
         on a.curriculum_id = b.id 
         where a.login_status = 1''')

        self.user_info = list(c.fetchall()[0])

        c.close()
        conn.close()

        # 유저의 현 상태와 커리큘럼 라벨 설정
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

        # 유저 번호 20만번 이하는 학생
        if self.user_info[0] < 200000:
            # 학생의 경우 입실, 복귀, 외출, 퇴실 시간을 표시해주며
            self.attend_time.setText(f'입실 시간 | {self.user_info[10]}')
            self.comeback_time.setText(f'복귀 시간 | {self.user_info[13]}')
            self.cut_off_time.setText(f'외출 시간 | {self.user_info[11]}')
            self.leave_time.setText(f'퇴실 시간 | {self.user_info[12]}')

            # 출결 여부도 함께 출력
            self.attend_status.setText(f'출석 {self.user_info[18] - self.user_info[14] - self.user_info[3]} '
                                       f'결석 {self.user_info[3]}, 지각 {self.user_info[4]}, 조퇴 {self.user_info[5]}, '
                                       f'외출 {self.user_info[6]}')

        # 교사의 경우 출퇴근 시간만 출력
        else:
            self.attend_time.setText(f'출근 시간 | {self.user_info[10]}')
            self.comeback_time.setText(f'퇴근 시간 | {self.user_info[12]}')
            self.cut_off_time.setText('')
            self.leave_time.setText('')
            self.attend_status.setText('')

    def set_user_status(self):
        # 학생인 경우의 유저 상태
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
        # 수업명을 받아오는 변수 선언
        user_curriculum = self.user_info[17]
        # 15글자 이상인 경우
        if len(user_curriculum) > 14:
            # 12글자에서 잘라줘서 맨 아랫쪽에 보기 흉하게 한두글자 내려가는 것을 방지함
            self.curriculum_title.setText(f'{user_curriculum[:12]}\n{user_curriculum[12:]}')
        else:
            self.curriculum_title.setText(user_curriculum)

    def set_btn(self):
        self.chat_btn.clicked.connect(self.chat)
        self.chat_btn.setGeometry(220, 400, 80, 40)

        self.log_out_btn.clicked.connect(self.log_out)
        self.log_out_btn.setGeometry(60, 460, 80, 40)

        self.close_btn.clicked.connect(self.quit_program)
        self.close_btn.setGeometry(220, 460, 80, 40)

        self.attend_btn.clicked.connect(self.change_user_status)
        self.cut_off_btn.clicked.connect(self.cut_off)

    # 반응형 버튼이 아닌 버튼들의 텍스트 세팅
    def set_btn_text(self):
        self.chat_btn.setText('상담')
        self.log_out_btn.setText('로그아웃')
        self.close_btn.setText('종료')

    # 버튼 활성화 함수
    def set_btn_activate(self):
        # 휴일 리스트 작성
        holiday = ['2023-01-24', '2023-03-02', '2023-05-08']
        # 금요일과 토요일 리스트
        weekend = [5, 6]
        # 유저가 출근 또는 입실 전인 경우의 버튼 세팅
        if self.user_info[8] == 0 and str(datetime.date.today()) not in holiday and \
                datetime.date.today().weekday() not in weekend:
            self.attend_btn.setGeometry(60, 400, 80, 40)

            if self.user_info[0] < 200000:
                self.attend_btn.setText('입실')

            else:
                self.attend_btn.setText('출근')

        # 유저가 출근 or 입실했을 경우
        elif self.user_info[8] == 1:
            self.attend_btn.setGeometry(60, 400, 80, 40)

            # 학생인 경우에 퇴실 텍스트 및 외출 버튼 출력함
            if self.user_info[0] < 200000:
                self.attend_btn.setText('퇴실')

                # 복귀 시간이 기본값인 경우 외출 버튼 활성화
                if not self.user_info[13]:
                    self.cut_off_btn.setGeometry(160, 400, 40, 40)
                    self.cut_off_btn.setText('외출')

            else:
                self.attend_btn.setText('퇴근')

        # 유저가 현재 외출 상태(교사는 외출 상태 진입 불가이기에 조건 x)인 경우 텍스트 복귀로 하여 버튼 활성화
        elif self.user_info[8] == 2:
            self.cut_off_btn.setGeometry(160, 400, 40, 40)
            self.cut_off_btn.setText('복귀')

    # 버튼 비활성화, 입실(출근)과 외출 버튼을 사라지게 만들어 선택 자체가 불가능하게끔 함
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
        # 텍스트 포멧 저장용 변수 설정
        fill_date_background = QTextCharFormat()
        # 해당 변수 배경을 노란색으로
        fill_date_background.setBackground(Qt.yellow)

        # 데이터 삭제시마다 노란색 배경을 제거할 수 있게끔 일정이 존재하지 않는 부분은 하얀 배경을 가지게 설정
        clear_date_background = QTextCharFormat()
        clear_date_background.setBackground(Qt.white)

        # 스케줄이 있는 날짜를 담아줄 리스트 선언
        scheduled_day = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 일정 삭제 상태가 참인 일정(프로그램 상 삭제했으나 DB에는 남아있는 일정)의 데이터를 가져와서
        c.execute('''SELECT DISTINCT DATE_FORMAT(the_day, "%Y-%m-%d") FROM korchamhrd.schedule_db 
        WHERE schedule_deleted = 1 ORDER BY the_day''')
        temp1 = list(c.fetchall())

        for i in range(len(temp1)):
            scheduled_day.append(temp1[i][0])

        for date in scheduled_day:
            the_day = QDate.fromString(date, "yyyy-MM-dd")
            # 해당 날 배경색을 하얀 색으로 되돌림
            self.calendar.setDateTextFormat(the_day, clear_date_background)

        # 스케줄 초기화
        scheduled_day = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 스케줄이 있는 날짜를 중복x로 받아옴
        c.execute('''SELECT DISTINCT DATE_FORMAT(the_day, "%Y-%m-%d") FROM korchamhrd.schedule_db 
        WHERE schedule_deleted=0 ORDER BY the_day''')
        temp = list(c.fetchall())

        c.close()
        conn.close()

        # 스케줄 날짜 리스트에 값 삽입
        for i in range(len(temp)):
            scheduled_day.append(temp[i][0])

        # 스케줄 데이 안에서
        for date in scheduled_day:
            # 해당 날을 문자열 형태에서(문자열 형태로 저장한 DB에서 가져왔으므로) 받아온 뒤
            the_day = QDate.fromString(date, "yyyy-MM-dd")
            # 받아온 날의 배경색을 채워줌
            self.calendar.setDateTextFormat(the_day, fill_date_background)

    # 캘린더 새로고침
    def refresh_calendar(self):
        # 캘린더 텍스트 배경색 설정을 매 초마다 무한반복
        while True:
            self.set_calendar_background()
            time.sleep(1)

    def schedule_management(self):
        # schedule_board.py 파일의 ScheduleBoard 클래스에 유저 정보와 달력에서 선택한 날을 상속받는 객체를 생성하고
        self.schedule_board = ScheduleBoard(self.user_info, self.calendar.selectedDate())
        # 새 창 출력
        self.schedule_board.show()

    def set_ui(self):
        self.set_label()
        self.set_label_text()
        self.set_btn()
        self.set_calendar()
        # 기본 폰트 D2Coding
        self.setFont(QtGui.QFont('D2Coding'))

    # DB와 UI 새로고침
    def refresh_db_ui(self):
        self.set_db()
        self.set_btn_text()
        self.set_btn_deactivate()
        self.set_btn_activate()
        self.set_label_text()
        self.set_user_status()

    # 출결 상태 변경 함수
    def change_user_status(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 입실 전 상태에서 해당 함수가 호출되었을 경우
        if self.user_info[8] == 0:
            # 유저 상태를 출석으로 변경하고
            self.user_info[8] = 1
            # 출석부 DB상에 시간을 적고 상태 변경, 24시간은 H, 12시간은 I를 사용함
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=1, 
            attend_time="{strftime('%H:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            # 입실 시간이 9시 20분 이후일 경우
            if int(strftime('%H%M')) > 920:
                # 지각 +1
                self.user_info[4] += 1
                # DB 적용
                c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET tardy={self.user_info[4]} 
                WHERE id={self.user_info[0]}''')
                conn.commit()

                # 결석 판정
                self.absence_increase()

            # 교수가 아닐 경우(교수의 과목 번호는 1) 입실, 교수의 경우 출근 메세지 출력
            self.attend_message('입실', '출근')

        # 입실 상태에서 해당 함수(입, 퇴실 버튼)가 호출된 경우
        elif self.user_info[8] == 1:
            # 상태를 퇴실에 해당하는 3으로 변경 및 DB 적용
            self.user_info[8] = 3
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=3, 
            leave_time="{strftime('%H:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            # 15시 50분 이전 퇴실했을 경우
            if int(strftime('%H%M')) < 1550:
                # 월요일과 금요일이 아니라면
                if datetime.date.today().weekday() != 0 and datetime.date.today().weekday() != 4:
                    # 16시 50분 이전 퇴실했을 경우
                    if int(strftime('%H%M')) < 1650:
                        # 조퇴 +1
                        self.user_info[5] += 1
                        c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` 
                        SET leave_early={self.user_info[5]} WHERE id={self.user_info[0]}''')
                        conn.commit()

                        self.absence_increase()

                # 월요일과 금요일은 그냥 +1
                else:
                    self.user_info[5] += 1
                    c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET leave_early={self.user_info[5]} 
                    WHERE id={self.user_info[0]}''')
                    conn.commit()

                    self.absence_increase()

            self.attend_message('퇴실', '퇴근')

        c.close()
        conn.close()

        # 새로 바뀐 DB와 버튼, 라벨 등 새로고침
        self.refresh_db_ui()

    # 외출 함수
    def cut_off(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 유저가 입실 상태인 경우
        if self.user_info[8] == 1:
            # 외출로 변경하고 외출 데이터를 DB에 작성
            self.user_info[8] = 2
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=2, 
            cut_time="{strftime('%H:%M')}" WHERE id={self.user_info[0]}''')
            conn.commit()

            QMessageBox.information(self, '외출', '외출하였습니다.')

        # 외출 상태에서 눌렀을 경우(복귀 버튼을 눌렀을 경우)
        elif self.user_info[8] == 2:
            self.user_info[8] = 1
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` SET user_status=1, 
            return_time="{strftime('%H:%M')}", period_cut={self.user_info[6] + 1} WHERE id={self.user_info[0]}''')
            conn.commit()

            QMessageBox.information(self, '복귀', '복귀하였습니다.')
            # 추가된 외출 횟수를 토대로 결석 판정
            self.absence_increase()

        c.close()
        conn.close()

        self.refresh_db_ui()

    # 출퇴근 메세지 출력 함수
    def attend_message(self, student_str, teacher_str):
        if self.user_info[9] != 1:
            QMessageBox.information(self, student_str, student_str + '하였습니다.')
        else:
            QMessageBox.information(self, teacher_str, teacher_str + '하였습니다.')

    def chat(self):
        self.chat_window = ChatWindow(self.user_info)
        self.chat_window.show()

    # 결석 판정기
    def absence_increase(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 지각, 조퇴, 외출의 합이 3의 배수일 때
        if (self.user_info[4] + self.user_info[5] + self.user_info[6]) % 3 == 0:
            # 결석 1회 추가하고 DB에 적용함
            self.user_info[3] += 1
            c.execute(f'''UPDATE korchamhrd.`{str(datetime.date.today())}` 
            SET absence={self.user_info[3]}, absence_record=1 WHERE id={self.user_info[0]}''')
            conn.commit()

        c.close()
        conn.close()

    def chat_alarm(self):
        while True:
            alarm_total = 0
            if self.user_info:
                conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
                c = conn.cursor()

                c.execute(f'SHOW TABLES LIKE "%{self.user_info[1]}%"')
                chat_room = c.fetchall()

                for i in range(len(chat_room)):
                    if self.user_info[0] < 200000:
                        pass
                    else:
                        c.execute(
                            f'SELECT COUNT(teacher_alarm) FROM korchamhrd.`{chat_room[i][0]}` WHERE teacher_alarm=1')
                        alarm_total += c.fetchall()[0][0]

                c.close()
                conn.close()

            else:
                pass

            if alarm_total != 0:
                self.chat_btn.setText(f'상담\n({str(alarm_total)})')
                pass


            else:
                self.chat_btn.setText('상담')

            time.sleep(1)

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
