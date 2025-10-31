from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget

res = {
  "RSA": {
    "MEXC": {
      "key": {
        "api-key": "",
        "secret": ""
      }
    },
    "Binance": {
      "key": {
        "api-key": "",
        "secret": ""
      },
      "торговля": {
        "price": "xxx",
        "quantity": "zzz"
      }
    },
    "OKX": {
      "key": {
        "api-key": "",
        "secret": ""
      },
      "индикаторы": {
        "boliger": {
          "x": "",
          "y": ""
        },
        "volume": {
          "x": "",
          "y": "",
          "z": ""
        }
      }
    },
    "Bybit": {
      "key": {
        "api-key": "",
        "secret": ""
      },
      "торговля": {
        "price": "xxx",
        "quantity": "zzz",
        "stop-loss": "xxx",
        "take-profit": "zzz"
      },
      "индикаторы": {
        "boliger": {
          "x": "",
          "y": ""
        },
        "volume": {
          "x": "",
          "y": "",
          "z": ""
        }
      }
    }
  },
  "СКОЛЬЗЯЧКАК": {
    "OKX": {
      "key": {
        "api-key": "",
        "secret": ""
      }
    }
  }
}

class TabsPage(QWidget):
    def __init__(self, parent=None, data=None, path=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Создаём QTabWidget для вкладок
        tab_widget = QTabWidget()
        
        # Получаем подсловарь на основе path
        current_data = self.get_current_data()
        
        # Автоматически создаём вкладки на основе ключей current_data
        for top_key, top_value in res.items():
            tab = QWidget()
            layout_tab = QVBoxLayout()
            
            # Добавляем название вкладки как метку (опционально, но полезно)
            label_title = QLabel(f"Раздел: {top_key}")
            layout_tab.addWidget(label_title)
            
            # Рекурсивно добавляем поля для top_value
            self.create_fields_for_dict(top_value, layout_tab)
            
            tab.setLayout(layout_tab)
            tab_widget.addTab(tab, top_key)
        
        # Добавляем QTabWidget в layout страницы
        layout.addWidget(tab_widget)
        
        # Создаём горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()
        
        # Кнопка "Старт"
        start_button = QPushButton("Старт")
        start_button.clicked.connect(self.on_start)
        buttons_layout.addWidget(start_button)
        
        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_button)
        
        # Добавляем кнопки в основной layout страницы
        layout.addLayout(buttons_layout)

    def create_fields_for_dict(self, d, layout):
        """Рекурсивно создаёт поля для словаря."""
        for key, value in d.items():
            if isinstance(value, dict):
                # Если значение — словарь, добавляем метку с ключом и рекурсивно поля
                label = QLabel(key)
                layout.addWidget(label)
                self.create_fields_for_dict(value, layout)
            else:
                # Если значение — строка, добавляем метку и поле ввода
                label = QLabel(key)
                layout.addWidget(label)
                edit = QLineEdit(value)  # Начальное значение из словаря
                layout.addWidget(edit)

    def on_start(self):
        if self.parent:
            self.parent.start_logging()

    def on_back(self):
        if self.parent:
            self.parent.switch_to_initial()
