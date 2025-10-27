import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QStackedWidget, QTextEdit, QLineEdit, QFormLayout,
    QGroupBox
)
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QFont
import time  # Для симуляции

class TradingThread(QThread):
    log_signal = Signal(str)  # Сигнал для отправки логов в GUI
    def __init__(self, exchange, server, strategy, settings):
        super().__init__()
        self.exchange = exchange
        self.server = server
        self.strategy = strategy
        self.settings = settings
        self.running = True

    def run(self):
        self.log_signal.emit("Запуск алгоритма...")
        # Здесь интегрируй реальный API Bybit. Пример с ccxt:
        # import ccxt
        # if self.server == "Тестовый":
        #     api = ccxt.bybit({"test": True})
        # else:
        #     api = ccxt.bybit()
        # api.apiKey = self.settings['api_key']
        # api.secret = self.settings['secret']
        # # Логика стратегии...

        # Плейсхолдер: Симуляция торговли
        while self.running:
            time.sleep(2)  # Симуляция задержки
            self.log_signal.emit(f"[{self.exchange}] [{self.server}] Стратегия: {self.strategy} - Проверка рынка...")
            self.log_signal.emit("Куплено 0.01 BTC по цене 50000 USDT")
            time.sleep(2)
            self.log_signal.emit("Продано 0.01 BTC по цене 50100 USDT")
            if not self.running:
                break
        self.log_signal.emit("Алгоритм остановлен.")

    def stop(self):
        self.running = False

class TradingBotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot by Bybit")
        self.setGeometry(100, 100, 600, 400)

        # Данные для передачи между экранами
        self.selected_exchange = ""
        self.selected_server = ""
        self.selected_strategy = ""
        self.settings = {}

        # QStackedWidget для экранов
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Экран 1: Выбор биржи
        self.screen1 = self.create_screen1()
        self.stack.addWidget(self.screen1)

        # Экран 2: Выбор сервера
        self.screen2 = self.create_screen2()
        self.stack.addWidget(self.screen2)

        # Экран 3: Выбор стратегии
        self.screen3 = self.create_screen3()
        self.stack.addWidget(self.screen3)

        # Экран 4: Настройки
        self.screen4 = self.create_screen4()
        self.stack.addWidget(self.screen4)

        # Экран 5: Запуск и логи
        self.screen5 = self.create_screen5()
        self.stack.addWidget(self.screen5)

        # Начать с экрана 1
        self.stack.setCurrentIndex(0)

    def create_screen1(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите биржу:"))
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(["Bybit"])  # Можно добавить другие
        layout.addWidget(self.exchange_combo)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.go_to_screen2)
        btn_layout.addWidget(btn_ok)
        # Back не нужен на первом экране
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def create_screen2(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите сервер:"))
        self.server_combo = QComboBox()
        self.server_combo.addItems(["Тестовый", "Боевой"])
        layout.addWidget(self.server_combo)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.go_to_screen3)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def create_screen3(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите стратегию:"))
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["Простая MA", "RSI", "Другая"])  # Примеры
        layout.addWidget(self.strategy_combo)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.go_to_screen4)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def create_screen4(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Настройки стратегии:"))
        
        # Форма настроек (зависит от стратегии, здесь общие)
        self.form_layout = QFormLayout()
        self.api_key_edit = QLineEdit()
        self.secret_edit = QLineEdit()
        self.amount_edit = QLineEdit("0.01")
        self.form_layout.addRow("API Key:", self.api_key_edit)
        self.form_layout.addRow("Secret:", self.secret_edit)
        self.form_layout.addRow("Amount:", self.amount_edit)
        layout.addLayout(self.form_layout)
        
        btn_layout = QHBoxLayout()
        btn_start = QPushButton("Start")
        btn_start.clicked.connect(self.start_trading)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def create_screen5(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Логи:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        btn_layout = QHBoxLayout()
        btn_stop = QPushButton("Stop")
        btn_stop.clicked.connect(self.stop_trading)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget

    def go_to_screen2(self):
        self.selected_exchange = self.exchange_combo.currentText()
        self.stack.setCurrentIndex(1)

    def go_to_screen3(self):
        self.selected_server = self.server_combo.currentText()
        self.stack.setCurrentIndex(2)

    def go_to_screen4(self):
        self.selected_strategy = self.strategy_combo.currentText()
        self.stack.setCurrentIndex(3)

    def start_trading(self):
        self.settings = {
            'api_key': self.api_key_edit.text(),
            'secret': self.secret_edit.text(),
            'amount': self.amount_edit.text()
        }
        self.stack.setCurrentIndex(4)
        self.trading_thread = TradingThread(self.selected_exchange, self.selected_server, self.selected_strategy, self.settings)
        self.trading_thread.log_signal.connect(self.update_log)
        self.trading_thread.start()

    def stop_trading(self):
        if hasattr(self, 'trading_thread'):
            self.trading_thread.stop()
        self.stack.setCurrentIndex(3)  # Назад к настройкам

    def update_log(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingBotApp()
    window.show()
    sys.exit(app.exec())
