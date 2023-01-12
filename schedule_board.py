import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QTextCharFormat
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QPushButton, QComboBox, QLineEdit, QMessageBox, \
    QTableWidget, QTableWidgetItem


class ScheduleBoard(QWidget):

    def __init__(self, user_info, calendar_date):
        super().__init__()
        self.user_info = user_info
        self.calendar_date = calendar_date
        self.schedule_db = ''

        self.window_title = QLabel(self)
        self.class_selected = QLabel(self)
        self.name_selected = QLabel(self)
        self.date_selected = QLabel(self)
        self.category_selected = QLabel(self)
        self.detail = QLabel(self)

        self.date_selected_show = QLineEdit(self)
        self.write_detail = QLineEdit(self)

        self.register_btn = QPushButton(self)
        self.delete_btn = QPushButton(self)
        self.close_btn = QPushButton(self)

        self.select_student_name = QComboBox(self)
        self.select_student_class = QComboBox(self)
        self.select_schedule_category = QComboBox(self)

        self.calendar = QCalendarWidget(self)
        self.schedule_board = QTableWidget(self)

        self.set_ui()
        # 창 실행시 스케줄 바로 표시
        self.show_schedule()

    def set_label(self):
        self.window_title.setText('개인별 특이사항')
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 00, 600, 40)
        self.setWindowIcon(QIcon('image/logo.png'))

        self.class_selected.setText('과정명')
        self.class_selected.setGeometry(350, 60, 40, 20)

        self.name_selected.setText('이  름')
        self.name_selected.setGeometry(350, 100, 40, 20)

        self.date_selected.setText('날  짜')
        self.date_selected.setGeometry(350, 140, 40, 20)

        self.category_selected.setText('분  류')
        self.category_selected.setGeometry(350, 180, 40, 20)

        self.detail.setText('상  세')
        self.detail.setGeometry(350, 220, 40, 20)

    def set_line(self):
        self.date_selected_show.setText(f'{self.calendar_date.toString("yyyy-MM-dd")}')
        self.date_selected_show.setReadOnly(True)
        self.date_selected_show.setGeometry(410, 140, 160, 20)

        self.write_detail.setGeometry(410, 220, 160, 20)
        self.write_detail.returnPressed.connect(self.register_schedule_process)

    def set_btn(self):
        self.register_btn.setText('등  록')
        self.register_btn.setGeometry(350, 260, 60, 20)
        self.register_btn.clicked.connect(self.register_schedule_process)

        self.delete_btn.setText('삭  제')
        self.delete_btn.setGeometry(430, 260, 60, 20)
        self.delete_btn.clicked.connect(self.delete_schedule)

        self.close_btn.setText('닫  기')
        self.close_btn.setGeometry(510, 260, 60, 20)
        self.close_btn.clicked.connect(self.close_board)

    def set_combo_box(self):
        self.select_student_class.clear()
        self.select_student_name.clear()

        self.select_student_class.setGeometry(410, 60, 160, 20)
        self.select_student_name.setGeometry(410, 100, 160, 20)

        # 10만번대는 학생이고 20만번대는 선생이야, 학생일 경우 본인의 정보만 콤보박스에서 선택이 가능
        if self.user_info[0] < 200000:
            self.select_student_class.addItem(self.user_info[17])
            self.select_student_name.addItem(self.user_info[3])

        # 교사인 경우 curriculum_db에서 현재 활성화된 모든 수업의 정보를 받아와서 콤보박스에 추가
        else:
            self.select_student_class.currentTextChanged.connect(self.set_teacher_combo_box)
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
            c = conn.cursor()

            c.execute('SELECT class_name FROM korchamhrd.curriculum_db WHERE class_status = 1')
            student_class = list(c.fetchall())

            for i in range(len(student_class)):
                self.select_student_class.addItem(student_class[i][0])
            # 학생들 이름을 콤보박스에 추가하는 함수 호출(교사모드)
            self.set_teacher_combo_box()
            c.close()
            conn.close()

        self.select_schedule_category.setGeometry(410, 180, 160, 20)
        schedule_category = ['과  제', '개인사', '병  가', '경조사']
        for i in range(len(schedule_category)):
            self.select_schedule_category.addItem(schedule_category[i], i)

    def set_teacher_combo_box(self):
        self.select_student_name.clear()
        # 콤보박스 과정명 교수인 경우 본인 이름만 선택 가능
        if self.select_student_class.currentText() == '교수':
            self.select_student_name.addItem(self.user_info[3])
        else:
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
            c = conn.cursor()

            # 과정명 선택에 따라 해당 과정 학생들만 출력
            c.execute(f'''SELECT user_name FROM korchamhrd.account_info AS a 
            INNER JOIN korchamhrd.curriculum_db AS b 
            ON a.curriculum_id=b.id 
            WHERE b.class_name="{self.select_student_class.currentText()}"''')
            student_name = list(c.fetchall())

            c.close()
            conn.close()

            for i in range(len(student_name)):
                self.select_student_name.addItem(student_name[i][0])

    def set_calendar(self):
        self.calendar.setGeometry(30, 60, 300, 220)
        self.calendar.setSelectedDate(self.calendar_date)
        self.calendar.clicked.connect(self.select_calendar_date)
        self.set_calendar_background_color()

    def set_schedule_board(self):
        self.schedule_board.setGeometry(30, 300, 540, 150)
        self.schedule_board.setColumnCount(5)
        self.schedule_board.setColumnWidth(0, 187)
        self.schedule_board.setColumnWidth(1, 55)
        self.schedule_board.setColumnWidth(2, 67)
        self.schedule_board.setColumnWidth(3, 43)
        self.schedule_board.setColumnWidth(4, 186)
        self.schedule_board.setHorizontalHeaderLabels(['과정', '이름', '날짜', '분류', '상세'])
        self.schedule_board.verticalHeader().setVisible(False)

    def set_ui(self):
        self.setGeometry(350, 300, 600, 480)
        self.setFont(QtGui.QFont('D2Coding'))
        self.setWindowTitle('일정 상황판')

        self.set_label()
        self.set_line()
        self.set_btn()
        self.set_combo_box()

        self.set_calendar()
        self.set_schedule_board()

    def select_calendar_date(self):
        self.show_schedule()
        # 선택된 날짜는 일정 등록부분의 날짜가 됨
        self.date_selected_show.setText(f'{self.calendar.selectedDate().toString("yyyy-MM-dd")}')

    # 달력 배경 색칠하기
    def set_calendar_background_color(self):
        # 텍스트 스타일 객체 생성
        fill_date_background = QTextCharFormat()
        # 해당 객체의 배경색을 노란색으로 함
        fill_date_background.setBackground(Qt.yellow)
        clear_date_background = QTextCharFormat()
        clear_date_background.setBackground(Qt.white)

        # 일정이 존재하는 날 변수 선언 및 초기화
        scheduled_day = []

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute('''SELECT DISTINCT DATE_FORMAT(the_day, "%Y-%m-%d") FROM korchamhrd.schedule_db 
        WHERE schedule_deleted = 1 ORDER BY the_day''')
        temp1 = list(c.fetchall())

        for i in range(len(temp1)):
            scheduled_day.append(temp1[i][0])

        for date in scheduled_day:
            # the_day 변수에 문자열을 날짜 형태로 변환하여 삽입
            the_day = QDate.fromString(date, "yyyy-MM-dd")
            # 해당하는 날짜에 함수 시작하며 만든 텍스트 스타일 적용
            self.calendar.setDateTextFormat(the_day, clear_date_background)

        scheduled_day = []
        # 삭제처리되지 않은 날짜 부분을 YYYY-MM-DD 형태의 텍스트로 받아옴
        c.execute('''SELECT DISTINCT DATE_FORMAT(the_day, "%Y-%m-%d") FROM korchamhrd.schedule_db 
        WHERE schedule_deleted = 0 ORDER BY the_day''')
        temp2 = list(c.fetchall())

        c.close()
        conn.close()

        # 받아와서 위에 선언한 변수에 삽입
        for i in range(len(temp2)):
            scheduled_day.append(temp2[i][0])

        for date in scheduled_day:
            the_day = QDate.fromString(date, "yyyy-MM-dd")
            self.calendar.setDateTextFormat(the_day, fill_date_background)

    def register_schedule_process(self):
        # DB에 일정 등록
        self.register_schedule_logic()
        # 라인에딧 초기화
        self.write_detail.clear()
        # 중복 방지 및 확인을 위한 알림창
        self.register_schedule_alarm()
        self.set_calendar_background_color()
        self.show_schedule()

    def register_schedule_logic(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        # 설정한 일정을 DB에 등록
        c.execute(f'''INSERT INTO korchamhrd.schedule_db VALUES(NULL, "{self.select_student_class.currentText()}",
        "{self.select_student_name.currentText()}", "{self.date_selected_show.text()}", 
        "{self.select_schedule_category.currentText()}", "{self.write_detail.text()}", 0, {self.user_info[0]})''')
        conn.commit()

        c.close()
        conn.close()

    def register_schedule_alarm(self):
        QMessageBox.information(self, '일정 등록', f'''{self.select_student_name.currentText()}님 
        {self.select_schedule_category.currentText()} 등록 완료''')

    def show_schedule(self):
        # 일정 DB를 읽어오고
        self.get_schedule_db()
        # 일정 DB를 출력함
        self.show_schedule_db()

    def get_schedule_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        c.execute(f'''SELECT id, class, student, DATE_FORMAT(the_day, "%Y-%m-%d"), category, detail 
        FROM korchamhrd.schedule_db WHERE the_day="{self.calendar.selectedDate().toString("yyyy-MM-dd")}"
        AND schedule_deleted=0''')
        self.schedule_db = c.fetchall()

        c.close()
        conn.close()

    def show_schedule_db(self):
        # 일정표 행 갯수 설정
        self.schedule_board.setRowCount(len(self.schedule_db))
        for i in range(len(self.schedule_db)):
            for j in range(1, len(self.schedule_db[i])):
                self.schedule_board.setItem(i, j - 1, QTableWidgetItem(self.schedule_db[i][j]))
            self.schedule_board.setVerticalHeaderItem(i, QTableWidgetItem(str(self.schedule_db[i][0])))

    def delete_schedule(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

        if self.schedule_board.currentRow() < 0:
            QMessageBox.warning(self, '대상 선택', '삭제하려는 일정을 선택하세요.')

        else:
            if self.user_info[0] >= 200000:
                c.execute(f'''UPDATE korchamhrd.schedule_db SET schedule_deleted=1
                WHERE id={int(self.schedule_board.verticalHeaderItem(self.schedule_board.currentRow()).text())}''')
                conn.commit()
                QMessageBox.information(self, '삭제 완료', '일정이 삭제되었습니다.')
                self.set_calendar_background_color()
                self.show_schedule()

            else:
                c.execute(f'''SELECT id FROM korchamhrd.schedule_db WHERE user_id={self.user_info[0]} 
                AND schedule_deleted=0''')
                temp = c.fetchall()
                if temp:
                    if temp[0][0] == int(self.schedule_board.verticalHeaderItem(self.schedule_board.currentRow()
                                                                                ).text()):
                        c.execute(f'''UPDATE korchamhrd.schedule_db SET schedule_deleted=1
                        WHERE id={int(self.schedule_board.verticalHeaderItem(self.schedule_board.currentRow()
                                                                             ).text())}''')
                        conn.commit()
                        QMessageBox.information(self, '삭제 완료', '일정이 삭제되었습니다.')
                        self.set_calendar_background_color()
                        self.show_schedule()

                    else:
                        QMessageBox.warning(self, '삭제 실패', '본인이 등록하지 않은 일정은\n삭제할 수 없습니다.')
                else:
                    QMessageBox.warning(self, '삭제 실패', '본인이 등록하지 않은 일정은\n삭제할 수 없습니다.')

        c.close()
        conn.close()

        self.show_schedule()

    def close_board(self):
        self.close()
