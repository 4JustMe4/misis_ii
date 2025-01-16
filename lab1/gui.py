import tkinter as tk
from tkinter import messagebox


class TranslatorAppGUI:
    def __init__(self, root, start_translation):
        self.word_input = tk.StringVar()
        self.source_language = tk.StringVar(value="en")
        self.target_language = tk.StringVar(value="ru")
        self.start_translation_callback = start_translation

        # Создание элементов GUI
        self.create_widgets(root)

    def create_widgets(self, root):
        # Элементы пользовательского интерфейса
        word_label = tk.Label(root, text="Введите текст для перевода:")
        word_label.pack()

        word_entry = tk.Entry(root, textvariable=self.word_input, width=50)
        word_entry.pack()

        source_lang_label = tk.Label(root, text="Выберите исходный язык:")
        source_lang_label.pack()

        source_lang_frame = tk.Frame(root)
        source_lang_frame.pack()

        en_source_button = tk.Radiobutton(
            source_lang_frame,
            text="Английский",
            variable=self.source_language,
            value="en",
        )
        ru_source_button = tk.Radiobutton(
            source_lang_frame, text="Русский", variable=self.source_language, value="ru"
        )
        en_source_button.pack(side=tk.LEFT)
        ru_source_button.pack(side=tk.LEFT)

        target_lang_label = tk.Label(root, text="Выберите целевой язык:")
        target_lang_label.pack()

        target_lang_frame = tk.Frame(root)
        target_lang_frame.pack()

        en_target_button = tk.Radiobutton(
            target_lang_frame,
            text="Английский",
            variable=self.target_language,
            value="en",
        )
        ru_target_button = tk.Radiobutton(
            target_lang_frame, text="Русский", variable=self.target_language, value="ru"
        )
        en_target_button.pack(side=tk.LEFT)
        ru_target_button.pack(side=tk.LEFT)

        start_button = tk.Button(root, text="Перевести", command=self.start_translation)
        start_button.pack()

        output_frame = tk.Frame(root)
        output_frame.pack()

        google_frame = tk.Frame(output_frame)
        google_frame.pack(side=tk.LEFT, padx=10)

        rapid_frame = tk.Frame(output_frame)
        rapid_frame.pack(side=tk.LEFT, padx=10)

        google_label = tk.Label(google_frame, text="Google Translator API:")
        google_label.pack()

        self.translation_text1 = tk.Text(google_frame, height=5, width=30)
        self.translation_text1.pack()

        rapid_label = tk.Label(rapid_frame, text="Rapid Translate API:")
        rapid_label.pack()

        self.translation_text2 = tk.Text(rapid_frame, height=5, width=30)
        self.translation_text2.pack()

    def start_translation(self):
        word = self.word_input.get()
        source_lang = self.source_language.get()
        target_lang = self.target_language.get()

        if not word:
            messagebox.showerror(
                "Input Error", "Пожалуйста, введите текст для перевода."
            )
            return

        # Получаем переводы
        translation_google, translation_rapid = self.start_translation_callback(
            word, source_lang, target_lang
        )

        # Выводим переводы в текстовые поля
        self.translation_text1.delete(1.0, tk.END)
        self.translation_text1.insert(tk.END, translation_google)
        self.translation_text2.delete(1.0, tk.END)
        self.translation_text2.insert(tk.END, translation_rapid)
