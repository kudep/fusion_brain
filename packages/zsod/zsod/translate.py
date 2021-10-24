import logging
import re

import requests
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from .helpers import log_exceptions
from .global_init import device


logger = logging.getLogger(__name__)


def saved_loading(cls, *args, **kwags):
    try:
        return cls.from_pretrained(*args, **kwags)
    except requests.exceptions.ConnectionError:
        return cls.from_pretrained(*args, **kwags, local_files_only=True)


with log_exceptions(logger):
    logger.info("preparing translator")
    tokenizer = saved_loading(AutoTokenizer, "Helsinki-NLP/opus-mt-en-ru")
    model = saved_loading(AutoModelForSeq2SeqLM, "Helsinki-NLP/opus-mt-en-ru")

    translator_en_ru = pipeline(
        task="translation",
        tokenizer=tokenizer,
        model=model,
        device=-1 if device.type == "cpu" else 0,
    )
    tokenizer = saved_loading(AutoTokenizer, "Helsinki-NLP/opus-mt-ru-en")
    model = saved_loading(AutoModelForSeq2SeqLM, "Helsinki-NLP/opus-mt-ru-en")

    translator_ru_en = pipeline(
        task="translation",
        tokenizer=tokenizer,
        model=model,
        device=-1 if device.type == "cpu" else 0,
    )
    # translator_en_ru = pipeline(
    #     task="translation",
    #     model="Helsinki-NLP/opus-mt-en-ru",
    #     device=-1 if device.type == "cpu" else 0,
    # )
    # translator_ru_en = pipeline(
    #     task="translation",
    #     model="Helsinki-NLP/opus-mt-ru-en",
    #     device=-1 if device.type == "cpu" else 0,
    # )
    logger.info("translator is ready")


def translate_en_ru(texts):
    return translator_en_ru(texts)


def translate_ru_en(texts):
    return translator_ru_en(texts)


def has_cyrillic(text):
    return bool(re.search("[а-яА-Я]", text))
