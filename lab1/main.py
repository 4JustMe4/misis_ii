import tkinter as tk
from gui import TranslatorAppGUI
from api import google_translation, rapid_translation


def start_translation(word, source_lang, target_lang):
    # Получаем перевод от Google API и Rapid API
    translation_google = google_translation(word, source_lang, target_lang)
    translation_rapid = rapid_translation(word, source_lang, target_lang)
    return translation_google, translation_rapid


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    root.title("API Translator App")
    root.geometry("600x300+150+150")

    app = TranslatorAppGUI(root, start_translation)

    root.mainloop()
