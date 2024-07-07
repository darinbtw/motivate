from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLayout, QMainWindow, QApplication, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
import sys
import os

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowIcon()
        self.main_menu()
        
    def main_menu(self):
        self.setWindowTitle('Motivatly - Мотивация')
        self.setFixedSize(600, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout1 = QVBoxLayout()

        self.hello = QLabel('''Приветствую в замечательном приложении, для продуктивных людей!
В этом приложении вы сможете отмечать свои задачи и составлять к ним дедлай, а если 
вы не сможете их выполнить/отметить, то применится некоторая блокировка, в которой все 
соц.сети, игры, будут выключатся до срока истечения таймера''')
        self.layout1.addWidget(self.hello)

        self.button_to_start = QPushButton('Войти в ваш личный кабинет')
        self.button_to_start.clicked.connect(self.my_door)
        self.layout1.addWidget(self.button_to_start)

        central_widget.setLayout(self.layout1)

    def my_door(self):
        central_widged = QWidget()
        self.setFixedSize(500,350)
        self.setCentralWidget(central_widged)
        self.setWindowTitle('Ваш личный кабинет')

        main_layout = QVBoxLayout()

        self.hello_you = QLabel('Здравствуйте, рады вас видеть!')
        main_layout.addWidget(self.hello_you)

        self.button_to_main_menu = QPushButton('Вернуться в главное меню')
        self.button_to_main_menu.clicked.connect(self.main_menu)
        self.button_to_main_menu.setFixedWidth(170)
        main_layout.addWidget(self.button_to_main_menu)

        righ_side = QHBoxLayout()
        righ_side.addStretch()

        self.right_side = QLabel('Впишите задачу, которую вы хотите выполнить')
        self.right_side.setAlignment(Qt.AlignRight)
        righ_side.addWidget(self.right_side)

        main_layout.addLayout(righ_side)

        #Поле где мы вписываем задачу
        input_zadacha_layout = QHBoxLayout()
        input_zadacha_layout.addStretch()
        self.input_zadacha = QLineEdit()
        self.input_zadacha.setFixedWidth(300)
        input_zadacha_layout.addWidget(self.input_zadacha)

        main_layout.addLayout(input_zadacha_layout)

        text_data = QHBoxLayout()
        text_data.addStretch()
        self.text_data = QLabel('Введите вашу дату дедлайна')
        text_data.addWidget(self.text_data)

        main_layout.addLayout(text_data)

        input_data_layout = QHBoxLayout()
        input_data_layout.addStretch()
        self.input_data = QLineEdit('Введите дату окончания(ГГГГ-ММ-ДД)')
        self.input_data.setFixedWidth(200)
        input_data_layout.addWidget(self.input_data)

        main_layout.addLayout(input_data_layout)

        self.text1 = QLabel('Ваши задачи:')
        main_layout.addWidget(self.text1)

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(465,100)
        self.text_edit.setReadOnly(True)

        with open('option.txt', 'r', encoding='UTF-8') as file:
            self.text_edit.setText(file.read())
        main_layout.addWidget(self.text_edit)

        central_widged.setLayout(main_layout)

def check_and_create_file(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write('')

def start():
    check_and_create_file('option.txt')
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()