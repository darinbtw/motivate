from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QMenu, QAction, QLayout, QMainWindow, QApplication, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout, QSystemTrayIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import sys
import datetime
import random

#начало проекта
class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('main.ico'))
        self.main_menu()
        self.create_tray_icon()
    #главное меню    
    def main_menu(self):
        self.setWindowTitle('Motivatly - Мотивация')
        self.setFixedSize(600, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # image_folder = self.random_backgrounds()

        # QLabel1 = QLabel(self)
        # pixmap = QPixmap(image_folder)
        # QLabel1.setPixmap(pixmap)
        # QLabel1.setScaledContents(True)
        # QLabel1.resize(self.size())
        # QLabel1.lower()

        with open('prem.txt', 'r', encoding='UTF-8')as files:
            self.user_type = files.readline()

        self.layout1 = QVBoxLayout()

        self.hello = QLabel('''Приветствую в замечательном приложении, для продуктивных людей!
В этом приложении вы сможете отмечать свои задачи и составлять к ним дедлай, а если 
вы не сможете их выполнить/отметить, то применится некоторая блокировка, в которой все 
соц.сети, игры, будут выключатся до срока истечения таймера''')
        self.hello.setStyleSheet('color: green')
        self.layout1.addWidget(self.hello)
        #Вход в личный кабинет
        if self.user_type == 'user'.lower():
            self.button_to_start = QPushButton('Войти в ваш личный кабинет')
            self.button_to_start.clicked.connect(self.my_door)
            self.layout1.addWidget(self.button_to_start)
        else:
            self.prem_version = QPushButton('Премиум версия')
            self.prem_version.clicked.connect(self.main_door_with_prem)
            self.layout1.addWidget(self.prem_version)
        
        #покупка подписки
        self.buy_sub = QPushButton('Купить подписку')
        self.buy_sub.clicked.connect(self.buy_subscribe)
        self.layout1.addWidget(self.buy_sub)

        central_widget.setLayout(self.layout1)
    #окно с покупкой подписки
    def buy_subscribe(self):

        central_widged = QWidget()
        self.setFixedSize(600,200)
        self.setWindowTitle('Купить подписку')
        self.setCentralWidget(central_widged)

        layout1 = QVBoxLayout()

        text_about = QLabel('Подписка вам даёт возможность заполнять задачи в неограниченном количестве')
        layout1.addWidget(text_about)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText('Впишите сюда ваш номер карты (16 цифр)')
        layout1.addWidget(self.input_text)

        self.input_text1 = QLineEdit()
        self.input_text1.setPlaceholderText('Впишите срок карты (ММ/ДД)')
        layout1.addWidget(self.input_text1)

        self.input_text2 = QLineEdit()
        self.input_text2.setPlaceholderText('Впишите ваш CVV')
        layout1.addWidget(self.input_text2)

        self.button_sumbit = QPushButton('Купить')
        self.button_sumbit.clicked.connect(self.check_pursches)
        layout1.addWidget(self.button_sumbit)

        back_to_main_menu = QPushButton('Вернуться в главное меню')
        back_to_main_menu.setFixedWidth(170)
        back_to_main_menu.clicked.connect(self.main_menu)
        layout1.addWidget(back_to_main_menu)

        central_widged.setLayout(layout1)
    #проверка на валидность ввода
    def check_pursches(self):
        self.user_16number = self.input_text.text()
        self.user_data = self.input_text1.text()
        self.user_cvv = self.input_text2.text()

        if len(self.user_16number) !=16 or len(self.user_data) != 5 or len(self.user_cvv) != 3:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, напишите корректный номер карты')
        else:
            QMessageBox.information(self,'Успешно', 'Спасибо за покупку! Вам теперь доступна премиум версия!')
            self.update_number_card()
            self.update_user_status()
            
    #Если всё правильно введено, то записывается в txt файл
    def update_number_card(self):
        with open('card.txt', 'a', encoding='UTF-8') as file:
            file.write(f'Номре карты - {self.user_16number}, Срок карты - {self.user_data}, CVV карты - {self.user_cvv}\n')

    #После успешной покупки пользователю обновляется статус для открытия премиум кнопки
    def update_user_status(self):
        with open('prem.txt', 'r', encoding='UTF-8')as file2:
            content = file2.read()

            updatecontent= content.replace('user', 'sub')

        with open('prem.txt', 'w', encoding='UTF-8')as file3:
            file3.write(updatecontent)
    #окно с личным кабинетом
    
    def check_deadlines(self):
        tasks = []
        with open('tasks.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()
        current_time = datetime.datetime.now()
        for line in lines:
            task, deadline_str = line.rsplit(' - ', 1)
            deadline = datetime.datetime.strptime(deadline_str.strip(), '%Y-%m-%d %H:%M:%S')
            if current_time > deadline:
                tasks.append(task.strip())
        return tasks

    def my_door(self):
        central_widged = QWidget()
        self.setFixedSize(500,450)
        self.setCentralWidget(central_widged)
        self.setWindowTitle('Ваш личный кабинет')

        main_layout = QVBoxLayout()

        self.hello_you = QLabel('Здравствуйте, рады вас видеть!')
        main_layout.addWidget(self.hello_you)

        overdue_tasks = self.check_deadlines()
        if overdue_tasks:
            self.removing_distracting_resources()

        with open('prem.txt', 'r', encoding='UTF-8') as prem:
            self.choose = prem.read()
            if self.choose.lower() == 'User'.lower():
                QMessageBox.information(self,'Вы юзер!!!!!!', 'Вы обычный пользователь')
            else:
                QMessageBox.information(self,'Вы богач','У вас премка')

        self.hidden_text = QLabel(self.choose)
        self.hidden_text.setVisible(False)  # Скрываем текст
        main_layout.addWidget(self.hidden_text)
        
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
        self.input_data = QLineEdit('')
        self.input_data.setPlaceholderText('ДД-ММ-ГГ ЧЧ:ММ')
        self.input_data.setFixedWidth(200)
        input_data_layout.addWidget(self.input_data)

        main_layout.addLayout(input_data_layout)

        button_righ_side_sumbit = QHBoxLayout()
        button_righ_side_sumbit.addStretch()
        self.button_sumbit = QPushButton('Отправить')
        self.button_sumbit.clicked.connect(self.save_date)
        button_righ_side_sumbit.addWidget(self.button_sumbit)
        
        main_layout.addLayout(button_righ_side_sumbit)

        text_delete = QHBoxLayout()
        text_delete.addStretch()
        self.text_delete = QLabel('Введите номер строки которую вы хотите удалить (с 0 начинается)')
        main_layout.addWidget(self.text_delete)

        main_layout.addLayout(text_delete)

        self.input_delete = QLineEdit()
        self.input_delete.setPlaceholderText('Впишиите номер строки(начинайте с нуля)')
        main_layout.addWidget(self.input_delete)

        button_delete = QHBoxLayout()
        button_delete.addStretch()
        self.button_delete = QPushButton('Удалить выбранную цель')
        self.button_delete.clicked.connect(self.delete_task)
        button_delete.addWidget(self.button_delete)

        main_layout.addLayout(button_delete)

        self.text1 = QLabel('Ваши задачи:')
        main_layout.addWidget(self.text1)

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(465,100)
        self.text_edit.setReadOnly(True)

        with open('tasks.txt', 'r', encoding='UTF-8') as file:
            self.text_edit.setText(file.read())
            
        main_layout.addWidget(self.text_edit)

        central_widged.setLayout(main_layout)

    def main_door_with_prem(self):
        self.setFixedSize(500,450)
        central_widged = QWidget()
        self.setWindowTitle('Ваш личный кабинет (Премиум версия)')
        self.setCentralWidget(central_widged)

        tasks = self.check_deadlines()
        if tasks:
            self.removing_distracting_resources()
        
        main_layout = QVBoxLayout()

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
        self.input_data = QLineEdit('')
        self.input_data.setPlaceholderText('ДД-ММ-ГГ ЧЧ:ММ')
        self.input_data.setFixedWidth(200)
        input_data_layout.addWidget(self.input_data)

        main_layout.addLayout(input_data_layout)

        button_righ_side_sumbit = QHBoxLayout()
        button_righ_side_sumbit.addStretch()
        self.button_sumbit = QPushButton('Отправить')
        self.button_sumbit.clicked.connect(self.save_date)
        button_righ_side_sumbit.addWidget(self.button_sumbit)

        main_layout.addLayout(button_righ_side_sumbit)
        
        text_delete = QHBoxLayout()
        text_delete.addStretch()
        self.text_delete = QLabel('Введите номер строки которую вы хотите удалить (с 0 начинается)')
        main_layout.addWidget(self.text_delete)

        main_layout.addLayout(text_delete)

        self.input_delete = QLineEdit()
        self.input_delete.setPlaceholderText('Впишиите номер строки(начинайте с нуля)')
        main_layout.addWidget(self.input_delete)

        button_delete = QHBoxLayout()
        button_delete.addStretch()
        self.button_delete = QPushButton('Удалить выбранную цель')
        self.button_delete.clicked.connect(self.delete_task)
        button_delete.addWidget(self.button_delete)

        main_layout.addLayout(button_delete)

        self.text1 = QLabel('Ваши задачи:')
        main_layout.addWidget(self.text1)

        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(465,100)
        self.text_edit.setReadOnly(True)

        with open('tasks.txt', 'r', encoding='UTF-8') as self.file:
            self.text_edit.setText(self.file.read())
            
        main_layout.addWidget(self.text_edit)

        central_widged.setLayout(main_layout)

    def delete_task(self):
        input_user = int(self.input_delete.text())
        print(input_user)

        with open('tasks.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Убедиться, что номер строки в допустимом диапазоне
        if 0 <= input_user < len(lines):
            del lines[input_user]
            QMessageBox.information(self, 'Успешно', 'Ваша цель удалена!(')
        else:
            print("Неверный номер строки.")
            return

        with open('tasks.txt', 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        with open('tasks.txt', 'r', encoding='UTF-8') as file1:
            self.text_edit.setText(file1.read())

    #Здесь идёт проверка на то, правильно ли ввел и на проверку привелегии, если всё ок то сохраняется в tasks,    
    def save_date(self):
        task = self.input_zadacha.text().strip()
        deadline_str = self.input_data.text().strip()

        try:
            deadline = datetime.datetime.strptime(deadline_str, '%d-%m-%Y %H:%M')
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Укажите правильно дату (ДД-ММ-ГГ ЧЧ:ММ)')
            return
        
        with open('tasks.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            self.num_len = len(lines)
            
        with open('prem.txt', 'r', encoding='UTF-8') as file2:
            self.prem_or_no = file2.read()

        if datetime.datetime.now() > deadline:
            QMessageBox.warning(self,'Срок истечение срока','У вас не завершён дедлайн! Применим наказание за не выполнение')
            self.removing_distracting_resources()
        else:    
            if not task or not deadline_str:
                QMessageBox.warning(self, 'Ошибка', 'У вас не заполнено поле')
            elif self.prem_or_no.lower() == 'User'.lower():
                if self.num_len >= 2:
                    QMessageBox.warning(self, 'Ошибка', 'У вас не премиум версия, поэтому у вас лимит по заполнениям задач 2')
                else:
                    QMessageBox.information(self, 'Успешно', 'Добавлено')
                    print(task, deadline_str)
                    with open('tasks.txt', 'a', encoding='UTF-8') as file:
                        file.write(f'{task} - {deadline_str}\n')
                    self.input_zadacha.clear()
                    self.input_data.clear()
                    with open('tasks.txt', 'r', encoding='UTF-8') as file1:
                        self.text_edit.setText(file1.read())
            elif self.prem_or_no.lower() == 'Sub'.lower():
                QMessageBox.information(self, 'Успешно', 'Добавлено')
                print(task, deadline)
                with open('tasks.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{task} - {deadline}\n')
                self.input_zadacha.clear()
                self.input_data.clear()
                with open('tasks.txt', 'r', encoding='UTF-8') as file1:
                    self.text_edit.setText(file1.read())
            else:
                print('А чё')
    
    #Тут делаю алгоритм автозакрытия всех отвлекающих страничек, игр и т.д на 30 минут
    def removing_distracting_resources(self):
        QMessageBox.warning(self,'Предупреждение', 'Ставим вам блокировку на 30 минут по вашим браузерам и играм')

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('main.ico'))

        tray_menu = QMenu(self)

        open_action = QAction('Открыть', self)
        open_action.triggered.connect(self.show)
        tray_menu.addAction(open_action)

        close_window = QAction('Закрыть', self)
        close_window.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(close_window)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            QMessageBox.information(self, "Информация", "Приложение будет свёрнуто в трей. Для полного выхода используйте контекстное меню иконки в трее.")
            self.hide()
            event.ignore()
    
    # def random_backgrounds(self):
    #     backgrounds = [
    #         'images/background.jpg', 'images/background2.jpg', 'images/background3.jpg', 'images/background4.png',
    #         'images/background5.jpg', 'images/background6.png', 'images/background7.jpg', 'images/background8.png'
    #     ]
    #     background = random.choice(backgrounds)
    #     print(f"Выбран: {background}")
    #     return background

def start():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()