from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLabel, QLayout, QMainWindow, QApplication
import sys

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 300)
        #self.setWindowIcon()
        self.setWindowTitle('Motivatly - Мотивация')
        
    def main_menu(self):
        central_widget = QWidget()
        self.centralWidget(central_widget)



def start():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()