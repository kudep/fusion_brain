import logging
import torch
from .processing_image import Preprocess
from .modeling_frcnn import GeneralizedRCNN
from .utils import Config, saved_loading
from transformers import VisualBertForQuestionAnswering, BertTokenizerFast
from . import translate
import pathlib
import re

# load models and model components
# frcnn_cfg = Config.from_pretrained("unc-nlp/frcnn-vg-finetuned")

# frcnn = GeneralizedRCNN.from_pretrained("unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)

# image_preprocess = Preprocess(frcnn_cfg)

# bert_tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
# visualbert_vqa = VisualBertForQuestionAnswering.from_pretrained("uclanlp/visualbert-vqa")
frcnn_cfg = saved_loading(Config, "unc-nlp/frcnn-vg-finetuned")

frcnn = saved_loading(GeneralizedRCNN, "unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)

image_preprocess = Preprocess(frcnn_cfg)

bert_tokenizer = saved_loading(BertTokenizerFast, "bert-base-uncased")
visualbert_vqa = saved_loading(VisualBertForQuestionAnswering, "uclanlp/visualbert-vqa")
ru_pat = re.compile("[а-я]", re.I)

# run frcnn

vqa_answers = pathlib.Path("/vqa_data/data/answers_vqa.txt").read_text().split("\n")


def img_question2answer(image, question):
    ru_flag = bool(ru_pat.search(question))
    if ru_flag:
        question = translate.ru2en(question)
    images, sizes, scales_yx = image_preprocess(image)
    output_dict = frcnn(
        images,
        sizes,
        scales_yx=scales_yx,
        padding="max_detections",
        max_detections=frcnn_cfg.max_detections,
        return_tensors="pt",
    )
    # add boxes and labels to the image

    # Very important that the boxes are normalized
    # normalized_boxes = output_dict.get("normalized_boxes")
    features = output_dict.get("roi_features")

    question = [question]

    inputs = bert_tokenizer(
        question,
        padding="max_length",
        max_length=20,
        truncation=True,
        return_token_type_ids=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors="pt",
    )

    output_vqa = visualbert_vqa(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        visual_embeds=features,
        visual_attention_mask=torch.ones(features.shape[:-1]),
        token_type_ids=inputs.token_type_ids,
        output_attentions=False,
    )
    # get prediction
    pred_vqa = output_vqa["logits"].argmax(-1)
    answer = vqa_answers[pred_vqa[0]]
    if ru_flag:
        return translate.en2ru(answer)
    else:
        return answer


print(img_question2answer("/vqa_data/data/dog.jpg", "Кто на траве?"))
print(img_question2answer("/vqa_data/data/dog.jpg", "Who is on the grass?"))
