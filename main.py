from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLayout, QMainWindow, QApplication, QVBoxLayout
import sys

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
        self.setCentralWidget(central_widged)
        self.setWindowTitle('Ваш личный кабинет')

        self.layout2 = QVBoxLayout()

        self.hello_you = QLabel('Здравствуйте, рады вас видеть!')
        self.layout2.addWidget(self.hello_you)

        self.layout2.addStretch()


        central_widged.setLayout(self.layout2)


def start():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()