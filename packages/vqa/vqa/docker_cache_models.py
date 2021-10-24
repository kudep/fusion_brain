from .processing_image import Preprocess
from .modeling_frcnn import GeneralizedRCNN
from .utils import Config, saved_loading
from transformers import VisualBertForQuestionAnswering, BertTokenizerFast
from . import translate


# load models and model components
# def init():
#     frcnn_cfg = Config.from_pretrained("unc-nlp/frcnn-vg-finetuned")

#     frcnn = GeneralizedRCNN.from_pretrained("unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)

#     image_preprocess = Preprocess(frcnn_cfg)

#     bert_tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
#     visualbert_vqa = VisualBertForQuestionAnswering.from_pretrained("uclanlp/visualbert-vqa")

#     translate.ru2en("Фраза.")
#     translate.en2ru("Phrase.")
def init():
    frcnn_cfg = saved_loading(Config, "unc-nlp/frcnn-vg-finetuned")

    frcnn = saved_loading(GeneralizedRCNN, "unc-nlp/frcnn-vg-finetuned", config=frcnn_cfg)

    image_preprocess = Preprocess(frcnn_cfg)

    bert_tokenizer = saved_loading(BertTokenizerFast, "bert-base-uncased")
    visualbert_vqa = saved_loading(VisualBertForQuestionAnswering, "uclanlp/visualbert-vqa")

    translate.ru2en("Фраза.")
    translate.en2ru("Phrase.")