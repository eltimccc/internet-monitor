import requests
import logging
import time
from logging.handlers import RotatingFileHandler
from ping3 import ping
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Настройка логгера
def setup_logger():
    logger = logging.getLogger("InternetMonitor")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        "internet_monitor.log", maxBytes=50 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()
monitoring = False  # Глобальная переменная для состояния мониторинга


def monitor_internet():
    while monitoring:
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                logger.info(f"Интернет есть. Пинг: {ping('www.google.com'):.2f} мс")
            else:
                logger.warning(f"Ошибка доступа к Google: статус {response.status_code}.")
        except requests.RequestException:
            logger.error("Интернет пропал.")
        time.sleep(60)


def toggle_monitoring():
    global monitoring
    monitoring = not monitoring  # Переключение состояния
    if monitoring:
        logger.info("Мониторинг запущен.")
        threading.Thread(target=monitor_internet, daemon=True).start()
        toggle_button.config(text="Остановить мониторинг", style="Stop.TButton")
    else:
        logger.info("Мониторинг остановлен.")
        toggle_button.config(text="Запустить мониторинг", style="Start.TButton")


def on_closing():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        global monitoring
        monitoring = False  # Останавливаем мониторинг перед выходом
        root.destroy()


# Интерфейс Tkinter
root = tk.Tk()
root.title("Монитор интернета")
root.geometry("300x150")  # Устанавливаем размер окна
root.resizable(False, False)  # Запрещаем изменение размеров окна

# Стили для кнопок
style = ttk.Style()
style.configure("Start.TButton", font=("Helvetica", 12), foreground="green")
style.configure("Stop.TButton", font=("Helvetica", 12), foreground="red")

# Кнопка для управления мониторингом
toggle_button = ttk.Button(root, text="Запустить мониторинг", style="Start.TButton", command=toggle_monitoring)
toggle_button.pack(pady=40)

# Обработка закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
