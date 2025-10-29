bybit_trading_bot/
        ├── gui/
        │    ├── windows/
        │    │     ├── init.py
        │    │     ├── main_win.py
        │    │     ├── initial_page.py
        │    │     ├── tabs_page.py
        │    │     ├── log_window.py
        │    │     ├── log_trade.py
        │    │     └── log_page.py
        │    └── styles/
        │          └── styles.qss
        ├── work_bot/
        │      ├── run_1/
        │      │     ├── init.py
        |      |     └── work.py
        │      └── run_2/
        │           ├── init.py
        │           └── work.py
        └── main.py

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time  # Для имитации задержек в потоке

# main_win.py
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Устанавливаем заголовок окна
        self.setWindowTitle("Динамическое окно с QStackedWidget")
        self.setGeometry(100, 100, 400, 300)
        
        # Создаём QStackedWidget для переключения страниц
        self.stacked_widget = QStackedWidget()
        
        # Создаём страницы
        self.create_initial_page()
        self.create_tabs_page()
        
        # Устанавливаем QStackedWidget как центральный виджет окна
        self.setCentralWidget(self.stacked_widget)

    def create_initial_page(self):
        self.initial_page = InitialPage(self)
        self.stacked_widget.addWidget(self.initial_page)
    
    def create_tabs_page(self):
        self.tabs_page = TabsPage(self)
        self.stacked_widget.addWidget(self.tabs_page)
   
    def switch_to_tabs(self):
        # Переключаемся на вторую страницу (индекс 1)
        self.stacked_widget.setCurrentIndex(1)
    
    def switch_to_initial(self):
        # Переключаемся на первую страницу (индекс 0)
        self.stacked_widget.setCurrentIndex(0)
    
    def start_logging(self):
        self.log_window = LogWindow()
        self.log_window.show()
        
        self.worker = LogThread()
        self.worker.log_signal.connect(self.log_window.append_log)
        # Подключаем кастомный сигнал завершения вместо стандартного finished
        self.worker.finished_signal.connect(self.log_window.append_log)
        # Подключаем сигнал закрытия окна к остановке потока
        self.log_window.closed.connect(self.worker.stop)
        self.worker.start()

# initial_page.py
class InitialPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
   
    def setup_ui(self):
        layout = QVBoxLayout(self)
    
        label = QLabel("Добро пожаловать! Это начальная страница.")
        layout.addWidget(label)
    
        button = QPushButton("Далее")
        button.clicked.connect(self.on_next)  # Слот внутри класса
        layout.addWidget(button)

    def on_next(self):
        # Логика переключения через parent
        if self.parent:
            self.parent.switch_to_tabs()

# tags_page.py
class TabsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
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
        start_button.clicked.connect(self.on_start)  # Исправлено: подключаем к on_start
        buttons_layout.addWidget(start_button)
        
        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.on_back)  # Исправлено: подключаем к on_back
        buttons_layout.addWidget(back_button)
        
        # Добавляем кнопки в основной layout страницы
        layout.addLayout(buttons_layout)

    def on_start(self):
        if self.parent:
            self.parent.start_logging()

    def on_back(self):
        if self.parent:
            self.parent.switch_to_initial()
      
# log_window.py
class LogWindow(QMainWindow):
    closed = Signal()  # Сигнал, который эмитится при закрытии окна
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно логов")
        self.setGeometry(500, 100, 400, 300)
        
        # Создаём страницы
        self.create_log_page()

    def create_log_page(self):
        self.log_page = LogPage(self)
        self.setCentralWidget(self.log_page)
    
    def append_log(self, message):
        # Делегируем вызов append_log в LogPage
        self.log_page.append_log(message)
        
    def closeEvent(self, event):
        self.closed.emit()  # Эмитим сигнал закрытия
        # Если MainWindow уже подключил сигналы, отключаем их (предполагаем, что worker существует)
        if hasattr(self, 'worker') and self.worker:
            self.worker.finished_signal.disconnect(self.append_log)  # Отключаем кастомный сигнал
        event.accept()  # Закрываем окно

# log_page.py
class LogPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Создаём QTextEdit для отображения логов
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        # Создаём кнопку "Завершить"
        self.finish_button = QPushButton("Завершить")
        self.finish_button.clicked.connect(self.on_finish)
        layout.addWidget(self.finish_button)
    
    def append_log(self, message):
        # Проверяем, видимо ли окно, чтобы избежать ошибок при попытке обновить закрытый виджет
        if self.isVisible():
            self.text_edit.append(message)
    
    def on_finish(self):
        if self.parent:
            self.parent.close()  # Закрывает LogWindow

# log_trade.py
class LogThread(QThread):
    log_signal = Signal(str)  # Сигнал для передачи сообщений
    finished_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True  # Флаг для контроля цикла
    
    def run(self):
        counter = 0
        while self.running:
            time.sleep(1)  # Имитируем задержку (1 секунда)
            self.log_signal.emit(f"Лог сообщение #{counter}")  # Эмитим сигнал с сообщением
            counter += 1
            if counter > 10:  # Останавливаемся после 10 сообщений для примера
                break
        # Эмитим кастомный сигнал завершения вместо стандартного finished
        self.finished_signal.emit("Логирование завершено!")

    def stop(self):
        self.running = False

# main.py
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
