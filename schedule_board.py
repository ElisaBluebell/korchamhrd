import pymysql

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QPushButton, QListWidget, QComboBox, QLineEdit


class ScheduleBoard(QWidget):

    def __init__(self, user_data, calendar_date):
        super().__init__()
        self.user_data = user_data
        self.calendar_date = calendar_date

        self.window_title = QLabel(self)
        self.class_selected = QLabel(self)
        self.name_selected = QLabel(self)
        self.date_selected = QLabel(self)
        self.category_selected = QLabel(self)
        self.detail = QLabel(self)

        self.date_selected_show = QLineEdit(self)
        self.detail_write = QLineEdit(self)

        self.register_btn = QPushButton(self)
        self.close_btn = QPushButton(self)

        self.select_student_name = QComboBox(self)
        self.select_student_class = QComboBox(self)
        self.select_schedule_category = QComboBox(self)

        self.calendar = QCalendarWidget(self)
        self.schedule_board = QListWidget(self)

        self.set_ui()

    def set_label(self):
        self.window_title.setText('개인별 특이사항')
        self.window_title.setFont(QtGui.QFont('D2Coding', 20))
        self.window_title.setAlignment(Qt.AlignCenter)
        self.window_title.setGeometry(0, 00, 600, 40)

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
        self.date_selected_show.setGeometry(410, 140, 150, 20)

        self.detail_write.setGeometry(410, 220, 150, 20)

    def set_btn(self):
        self.register_btn.setText('등  록')
        self.register_btn.setGeometry(350, 260, 60, 20)
        self.register_btn.clicked.connect(self.register_schedule)

        self.close_btn.setText('닫  기')
        self.close_btn.setGeometry(490, 260, 60, 20)
        self.close_btn.clicked.connect(self.close_board)

    def set_combo_box(self):
        self.select_student_class.clear()
        self.select_student_name.clear()

        self.select_student_class.setGeometry(410, 60, 150, 20)
        self.select_student_name.setGeometry(410, 100, 150, 20)

        # 10만번대는 학생이고 20만번대는 선생이야, 학생일 경우 본인의 정보만 콤보박스에서 선택이 가능
        if self.user_data[0] < 200000:
            self.select_student_class.addItem(self.user_data[12])
            self.select_student_name.addItem(self.user_data[3])

        # 교사인 경우 curriculum_db에서 모든 수업의 정보를 받아와서 콤보박스에 추가
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

        self.select_schedule_category.setGeometry(410, 180, 150, 20)
        schedule_category = ['과  제', '개인사', '병  가', '경조사']
        for i in range(len(schedule_category)):
            self.select_schedule_category.addItem(schedule_category[i], i)

    def set_teacher_combo_box(self):
        self.select_student_name.clear()
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='korchamhrd')
        c = conn.cursor()

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
        self.calendar.clicked.connect(self.set_calendar_date)

    def set_schedule_board(self):
        self.schedule_board.setGeometry(30, 300, 540, 150)

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

    def set_calendar_date(self):
        self.date_selected_show.setText(f'{self.calendar.selectedDate().toString("yyyy-MM-dd")}')

    def register_schedule(self):
        pass

    def close_board(self):
        self.close()
