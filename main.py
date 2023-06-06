import asyncio
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QGridLayout, \
    QTextEdit, QPlainTextEdit, QLineEdit
from asyncqt import QEventLoop

from send_appeal import send
from settings import get_server_url, save_server_url


class CitizenAppeal(QMainWindow):
    def __init__(self):
        # Инициализация родительского класса
        super().__init__()
        # Установка заголовка окна
        self.setWindowTitle('Прием обращений от граждан')

        # Создание табличного макета
        grid = QGridLayout()

        # Создание виджета
        widget = QWidget()
        # Установка табличного макета в виджет
        widget.setLayout(grid)
        # Установка виджета в центральный виджет окна
        self.setCentralWidget(widget)

        self.name_caption = QLabel(self)
        self.name_caption.setText('Имя:')
        self.name_edit = QLineEdit(self)

        self.email_caption = QLabel(self)
        self.email_caption.setText('Почта')
        self.email_edit = QLineEdit(self)

        self.text_caption = QLabel(self)
        self.text_caption.setText('Тест обращения')
        self.text_edit = QTextEdit(self)

        self.send_button = QPushButton(self)
        self.send_button.setText("Отправить")
        self.send_button.setStyleSheet("background-color:white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:15px;\n"
                                       "border-color:black;")
        self.server_api_edit = QLineEdit(self)

        self.answer_edit = QPlainTextEdit(self)
        self.answer_edit.setReadOnly(True)

        grid.addWidget(self.name_caption, 0, 0, alignment=Qt.AlignTop)
        grid.addWidget(self.name_edit, 0, 1)
        grid.addWidget(self.email_caption, 1, 0, alignment=Qt.AlignTop)
        grid.addWidget(self.email_edit, 1, 1)
        grid.addWidget(self.text_caption, 2, 0, alignment=Qt.AlignTop)
        grid.addWidget(self.text_edit, 2, 1)

        grid.addWidget(self.send_button, 3, 0)
        grid.addWidget(self.server_api_edit, 3, 1)

        grid.addWidget(self.answer_edit, 4, 0, 1, 2)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        grid.setRowStretch(3, 1)
        grid.setRowStretch(4, 1)

        # действие при нажатии на кнопку
        self.send_button.clicked.connect(self.send_appeal)

        url = get_server_url()

        self.server_api_edit.setText(url)

        print(url)

    def send_appeal(self):
        # кнопку делаем не доступной, что бы избежать повторного нажатия
        self.send_button.setEnabled(False)

        save_server_url(self.server_api_edit.text())
        # запуск асинхронной таски
        asyncio.create_task(self.run_send_appeal_operation())

    async def run_send_appeal_operation(self):
        # отправка на сервер тоже асинхронная
        result_from_server = await send(self.server_api_edit.text(),
                                        self.name_edit.text(), self.email_edit.text(),
                                        self.text_edit.toPlainText())
        # ответ показываем
        self.answer_edit.setPlainText(str(result_from_server))
        # кнопку делаем доступной
        self.send_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    si = CitizenAppeal()
    si.showMaximized()
    with loop:
        loop.run_forever()
