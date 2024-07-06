from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLayout, QMainWindow, QApplication, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
import sys
import os

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowIcon()
        self.setWindowTitle('Motivatly - Мотивация')
        self.main_menu()
        
    def main_menu(self):
        self.setFixedSize(500, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout1 = QVBoxLayout()

        self.hello = QLabel('''Приветствую в замечательном приложении, для продуктивных людей!
В этом приложении вы сможете отмечать свои задачи и составлять к ним дедлай, а если вы не сможете
их выполнить/отметить, то применится некоторая блокировка, в которой все соц.сети, игры, будут выключатся до срока истечения таймера''')
        self.layout1.addWidget(self.hello)

        self.button_to_start = QPushButton('Войти в ваш личный кабинет')
        self.button_to_start.clicked.connect(self.my_door)
        self.layout1.addWidget(self.button_to_start)

        central_widget.setLayout(self.layout1)

    def my_door(self):
        central_widged = QWidget()
        self.setFixedSize(500,250)
        self.setCentralWidget(central_widged)
        self.setWindowTitle('Ваш личный кабинет')

        self.layout2 = QVBoxLayout()

        self.hello_you = QLabel('Здравствуйте, рады вас видеть!')
        self.layout2.addWidget(self.hello_you)

        self.right_side = QLabel('Впишите задачу, которую вы хотите выполнить')
        self.right_side.setAlignment(Qt.AlignRight)
        self.layout2.addWidget(self.right_side)

        self.layout2.addStretch()

        self.text1 = QLabel('Ваши задачи:')
        self.layout2.addWidget(self.text1)

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(200,200)
        self.text_edit.setReadOnly(True)

        with open('option.txt', 'r', encoding='UTF-8') as file:
            self.text_edit.setText(file.read())
        self.layout2.addWidget(self.text_edit)



        central_widged.setLayout(self.layout2)

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