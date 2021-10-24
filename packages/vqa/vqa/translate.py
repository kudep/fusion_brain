import logging
from transformers import FSMTTokenizer, FSMTForConditionalGeneration

from .utils import saved_loading


logger = logging.getLogger(__name__)


class translator:
    def __init__(self, name_model):
        self.tokenizer = saved_loading(FSMTTokenizer, name_model)
        self.model = saved_loading(FSMTForConditionalGeneration, name_model)

    def translate_phrase(self, question):
        input_ids = self.tokenizer.encode(question, return_tensors="pt")
        outputs = self.model.generate(input_ids)
        decode = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decode


def preproc_phrase(phrase):
    if len(phrase) == 0:
        return phrase
    else:
        return phrase[0].upper() + phrase[1:]


def translate_batch(batch, ru_eng_translator, eng_ru_translator, ques_or_ans_key="question"):
    for dict_ in batch:
        if dict_["lang"] == "ru":
            if ques_or_ans_key == "question":
                dict_[f"{ques_or_ans_key}_translate"] = eng_ru_translator.translate_phrase(
                    preproc_phrase(dict_[ques_or_ans_key])
                )
            elif ques_or_ans_key == "answer":
                dict_[f"{ques_or_ans_key}_translate"] = ru_eng_translator.translate_phrase(
                    preproc_phrase(dict_[ques_or_ans_key])
                )
        elif dict_["lang"] == "en":
            if ques_or_ans_key == "question":
                dict_[f"{ques_or_ans_key}_translate"] = ru_eng_translator.translate_phrase(
                    preproc_phrase(dict_[ques_or_ans_key])
                )
            elif ques_or_ans_key == "answer":
                dict_[f"{ques_or_ans_key}_translate"] = eng_ru_translator.translate_phrase(
                    preproc_phrase(dict_[ques_or_ans_key])
                )


ru_eng_translator = translator("facebook/wmt19-ru-en")
eng_ru_translator = translator("facebook/wmt19-en-ru")


def ru2en(phrase):
    return ru_eng_translator.translate_phrase(preproc_phrase(phrase))


def en2ru(phrase):
    return eng_ru_translator.translate_phrase(preproc_phrase(phrase))
