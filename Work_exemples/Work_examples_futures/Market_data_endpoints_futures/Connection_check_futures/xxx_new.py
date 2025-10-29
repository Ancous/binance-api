import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QTextEdit, QHBoxLayout
from PySide6.QtCore import QThread, Signal

# Создаём основное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Устанавливаем заголовок окна
        self.setWindowTitle("Динамическое окно с QStackedWidget")
        self.setGeometry(100, 100, 400, 300)
        
        # Создаём QStackedWidget для переключения страниц
        self.stacked_widget = QStackedWidget()
        
        # Создаём первую страницу: вкладка с кнопкой "Далее"
        self.create_initial_page()
        
        # Создаём вторую страницу: две вкладки с кнопками
        self.create_tabs_page()
        
        # Устанавливаем QStackedWidget как центральный виджет окна
        self.setCentralWidget(self.stacked_widget)
    
    def create_initial_page(self):
        # Создаём страницу (виджет)
        page = QWidget()
        layout = QVBoxLayout()
        
        # Добавляем лейбл и кнопку
        label = QLabel("Добро пожаловать! Нажмите 'Далее' для перехода к двум вкладкам.")
        button = QPushButton("Далее")
        button.clicked.connect(self.switch_to_tabs)  # Подключаем обработчик
        
        layout.addWidget(label)
        layout.addWidget(button)
        page.setLayout(layout)
        
        # Добавляем страницу в QStackedWidget
        self.stacked_widget.addWidget(page)
    
    def create_tabs_page(self):
        # Создаём контейнер для второй страницы
        page = QWidget()
        layout = QVBoxLayout()
        
        # Создаём QTabWidget для вкладок
        tab_widget = QTabWidget()
        
        # Первая вкладка
        tab1 = QWidget()
        layout1 = QVBoxLayout()
        label1 = QLabel("Это первая вкладка после перехода!")
        layout1.addWidget(label1)
        tab1.setLayout(layout1)
        tab_widget.addTab(tab1, "Вкладка 1")
        
        # Вторая вкладка
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        label2 = QLabel("Это вторая вкладка после перехода!")
        layout2.addWidget(label2)
        tab2.setLayout(layout2)
        tab_widget.addTab(tab2, "Вкладка 2")
        
        # Добавляем QTabWidget в layout страницы
        layout.addWidget(tab_widget)
        
        # Создаём горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()
        
        # Кнопка "Старт"
        start_button = QPushButton("Старт")
        start_button.clicked.connect(self.start_logging)
        buttons_layout.addWidget(start_button)
        
        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.switch_to_initial)
        buttons_layout.addWidget(back_button)
        
        # Добавляем кнопки в основной layout страницы
        layout.addLayout(buttons_layout)
        
        page.setLayout(layout)
        
        # Добавляем страницу в QStackedWidget
        self.stacked_widget.addWidget(page)
    
    def switch_to_tabs(self):
        # Переключаемся на вторую страницу (индекс 1)
        self.stacked_widget.setCurrentIndex(1)
    
    def switch_to_initial(self):
        # Переключаемся на первую страницу (индекс 0)
        self.stacked_widget.setCurrentIndex(0)
    
    def start_logging(self):
        # Создаём новое окно для логов
        self.log_window = LogWindow()
        self.log_window.show()
        
        # Запускаем поток для имитации логов
        self.worker = LogWorker()
        self.worker.log_signal.connect(self.log_window.append_log)  # Подключаем сигнал к обновлению логов
        self.worker.finished.connect(lambda: self.log_window.append_log("Логирование завершено!"))  # Сообщение по окончании
        self.worker.start()  # Запускаем поток

# Класс для нового окна с логами
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно логов")
        self.setGeometry(500, 100, 400, 300)
        
        # Создаём QTextEdit для отображения логов
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Только для чтения
        
        # Создаём кнопку "Завершить"
        self.finish_button = QPushButton("Завершить")
        self.finish_button.clicked.connect(self.finish_logging)  # Подключаем слот
        
        # Компоновка: текст сверху, кнопка снизу
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.finish_button)
        
        # Центральный виджет с компоновкой
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Создаём и запускаем поток
        self.worker = LogWorker()
        self.worker.log_signal.connect(self.append_log)  # Подключаем сигнал
        self.worker.start()  # Запускаем поток сразу
    
    def append_log(self, message):
        # Добавляем сообщение в конец текста
        self.text_edit.append(message)
    
    def finish_logging(self):
        # Мягкое завершение: останавливаем поток и закрываем окно
        self.worker.running = False
        self.worker.wait()  # Ждём завершения потока
        self.close()  # Закрываем окно
    
    def closeEvent(self, event):
        # Останавливаем поток при закрытии окна (резерв, если крестик)
        self.worker.running = False
        self.worker.wait()  # Ждём завершения потока
        event.accept()  # Закрываем окно


# Класс для потока, имитирующего бесконечное логирование
class LogWorker(QThread):
    log_signal = Signal(str)  # Сигнал для передачи сообщений
    
    def __init__(self):
        super().__init__()
        self.running = True  # Флаг для контроля цикла
    
    def run(self):
        import time
        counter = 0
        while self.running:
            counter += 1
            self.log_signal.emit(f"Лог {counter}: Сообщение в {time.strftime('%H:%M:%S')}")
            time.sleep(1)  # Задержка 1 секунда между логами
        # После выхода из цикла поток завершится


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
