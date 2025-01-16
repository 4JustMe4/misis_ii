import tkinter as tk
from interface import TextGeneratorApp


if __name__ == "__main__":
    config_file = "config.yaml"
    root = tk.Tk()
    try:
        app = TextGeneratorApp(root, config_file)
    except Exception as e:
        print(f"Ошибка при инициализации приложения: {e}")
    root.mainloop()
