from transformers import GPT2LMHeadModel, GPT2Tokenizer
import yaml
from typing import Tuple, Union, Optional, Dict, Any


def load_config(file_path: str) -> Dict[str, Any]:
    """
    Загружает параметры конфигурации из файла .yaml.

    :param file_path: Путь к файлу конфигурации .yaml
    :return: Словарь с параметрами конфигурации
    """
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def load_tokenizer_and_model(
    model_name: str,
) -> Tuple[Optional[GPT2Tokenizer], Optional[GPT2LMHeadModel]]:
    """
    Загружает токенизатор и модель на основе указанного имени модели.

    :param model_name: Имя или путь модели
    :return: Кортеж из токенизатора и модели, либо (None, None) в случае ошибки
    """
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name).to("cpu")
        return tokenizer, model
    except Exception as e:
        print(f"Ошибка при загрузке модели {model_name}: {e}")
        return None, None


def generate_text(
    model: GPT2LMHeadModel,
    tokenizer: GPT2Tokenizer,
    text: str,
    config: Dict[str, Union[int, float, str]],
) -> str:
    """
    Генерирует текст с использованием модели и параметров из конфигурации.

    :param model: Загруженная модель GPT-2
    :param tokenizer: Загруженный токенизатор
    :param text: Исходный текст для генерации
    :param config: Словарь с параметрами генерации текста
    :return: Сгенерированный текст или сообщение об ошибке
    """
    if model is None or tokenizer is None:
        return "Ошибка: Модель не загружена."

    try:
        input_ids: list[int] = tokenizer.encode(text, return_tensors="pt")
        output_ids = model.generate(
            input_ids,
            max_length=int(config["max_length"]),
            repetition_penalty=float(config["repetition_penalty"]),
            do_sample=True,
            top_k=int(config["top_k"]),
            top_p=float(config["top_p"]),
            temperature=float(config["temperature"]),
            num_beams=int(config["num_beams"]),
            no_repeat_ngram_size=int(config["no_repeat_ngram_size"]),
        )
        generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        print(f"Ошибка при генерации текста: {e}")
        return "Ошибка: Не удалось сгенерировать текст."
