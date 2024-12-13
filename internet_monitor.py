import requests
import logging
import time
from logging.handlers import RotatingFileHandler
from ping3 import ping
import threading
import tkinter as tk
from tkinter import messagebox

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    "internet_monitor.log", maxBytes=50 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

monitoring = False


def monitor_internet():
    global monitoring
    while monitoring:
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                ping_time = ping("www.google.com")
                logger.info(f"Интернет есть. Пинг: {ping_time:.2f} мс")
            else:
                logger.warning(
                    f"Ошибка доступа к Google: статус {response.status_code}."
                )
        except requests.RequestException:
            logger.error("Интернет пропал.")
        time.sleep(60)


def start_monitoring():
    global monitoring
    monitoring = True
    logger.info("Мониторинг запущен.")
    threading.Thread(target=monitor_internet, daemon=True).start()


def stop_monitoring():
    global monitoring
    monitoring = False
    logger.info("Мониторинг остановлен.")


def on_closing():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        stop_monitoring()
        root.destroy()


root = tk.Tk()
root.title("Монитор интернета")

start_button = tk.Button(root, text="Пуск", command=start_monitoring)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Стоп", command=stop_monitoring)
stop_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
