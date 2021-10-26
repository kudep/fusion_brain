import json
from typing import Dict, List


def select_annotations_by_class_name(annotations, class_name):
    return {
        annotator_name: annotator_data["payload"]
        for annotator_name, annotator_data in annotations.items()
        if annotator_data["class"] == class_name
    }


def base_formatter_in(dialog: Dict, model_args_names=("raw_input",)):
    raw_data = json.loads(dialog["utterances"][-1]["text"])
    annotations = dialog["utterances"][-1].get("annotations", {})
    hypotheses = dialog["utterances"][-1].get("hypotheses", [])
    # print(f"base_formatter_in = {annotations.keys()}", flush=True)
    data = {
        "annotations": select_annotations_by_class_name(annotations, "annotator"),
        "post_annotations": select_annotations_by_class_name(annotations, "post_annotator"),
        "solvers": [{hyp["skill_name"]: json.loads(hyp["text"])} for hyp in hypotheses],
    }
    data.update(raw_data)
    return [{"input_data": [data]}]


def base_formatter_out(payload: List, confidence=0.5):
    return [{"text": json.dumps(payload), "confidence": 0.5}]


def base_annotator_formatter_out(payload: List):
    # print(f"base_annotator_formatter_out payload = {payload.keys()}")
    service_class = "annotator"
    if not payload:
        print(f"Warning: Empty payload provided by {service_class}")
    return {"payload": payload, "class": service_class}


def base_post_annotator_formatter_out(payload: List):
    # print(f"base_post_annotator_formatter_out payload = {payload.keys()}")
    service_class = "post_annotator"
    if not payload:
        print(f"Warning: Empty payload provided by {service_class}")
    return {"payload": payload, "class": service_class}


def response_selector_formatter_out(payload: Dict):
    # print(f"response_selector_formatter_out payload = {payload.keys()}")
    service_class = "response_selector"
    if not isinstance(payload, dict):
        print(f"Warning: Not a dict payload provided by {service_class}")
    return {"skill_name": "response_selector", "text": json.dumps(payload), "confidence": 1}
