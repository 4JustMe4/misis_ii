import tkinter as tk
from tkinter import scrolledtext
from text_generation import load_tokenizer_and_model, generate_text, load_config
from typing import Optional


class TextGeneratorApp:
    def __init__(self, root: tk.Tk, config_file: str):
        """
        Инициализирует приложение для генерации текста.

        :param root: Корневое окно tkinter
        :param config_file: Путь к файлу конфигурации .yaml
        """
        self.root = root
        self.root.title("Генератор текста с GPT-2")
        self.root.geometry("600x600")

        # Загружаем конфигурацию и модель
        self.config = load_config(config_file)
        self.tokenizer, self.model = load_tokenizer_and_model(self.config["model_name"])
        if self.tokenizer is None or self.model is None:
            self.show_error_message("Ошибка: Модель или токенизатор не были загружены.")
            return

        # Поле ввода текста
        tk.Label(root, text="Введите начальный текст:").pack(pady=10)
        self.input_text_entry = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=60, height=5
        )
        self.input_text_entry.pack(pady=5)

        # Кнопка для генерации текста
        generate_button = tk.Button(
            root, text="Сгенерировать текст", command=self.on_generate
        )
        generate_button.pack(pady=10)

        # Поле вывода текста
        self.output_text_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=60, height=10
        )
        self.output_text_display.pack(pady=5)

    def show_error_message(self, message: str):
        """
        Выводит сообщение об ошибке в интерфейсе.

        :param message: Сообщение об ошибке
        """
        self.output_text_display.insert(tk.END, f"{message}\n")

    def on_generate(self):
        """
        Обрабатывает нажатие кнопки "Сгенерировать текст",
        извлекает текст и отображает результат генерации.
        """
        self.output_text_display.delete("1.0", tk.END)

        input_text = self.input_text_entry.get("1.0", tk.END).strip()
        if not input_text:
            self.show_error_message("Введите начальный текст для генерации.")
            return

        try:
            generated_text = generate_text(
                self.model, self.tokenizer, input_text, self.config
            )
            self.output_text_display.insert(tk.END, f"{generated_text}\n\n")
        except Exception as e:
            self.show_error_message(f"Ошибка при генерации текста: {e}")
