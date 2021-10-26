import copy
import json

from cp_data_readers.map_update import SUBJECT_LIST

reduction2subject = {
    "rus": "русский язык",
    "lit": "литература",
    "his": "история",
    "hist": "история",
    "soc": "обществознание",
    "obch": "обществознание",
    "eng": "английский",
    "en": "английский",
}
for sub in reduction2subject.values():
    assert sub in SUBJECT_LIST


def create_instance(file):
    try:
        raw_input = file.open().read()
    except Exception:
        raw_input = file.open(encoding="windows-1251").read()
    txt_path = str(file)

    if "neznaika" in txt_path:
        instance = json.loads(raw_input)
        instance["instance_info"]["subject"] = "eng"
        instance["instance_info"]["file_name"] = file.name
    elif "prochtenie" in txt_path or "pku" in txt_path:
        raw_input = json.loads(raw_input)
        instance = {
            "raw_input": raw_input,
            "instance_info": {
                "dataset_split": "train" if "train" in txt_path else "test",
                "dataset_name": "prochtenie",
                "dataset_version": "v4",
                "subject": raw_input.get("meta", {}).get("subject", "eng"),
                "file_name": file.name,
            },
        }
    else:
        raise "not implemented"
    return instance


def get_dataset_files(dataset_path):
    if "neznaika" in str(dataset_path):
        mask = "./**/*.json"
    elif "prochtenie" in str(dataset_path):
        mask = "./**/*.json"
    else:
        raise ValueError("Unknown dataset")
    return list(dataset_path.glob(mask))


selection_keys2type = {
    "comment": str,
    "correction": str,
    "endSelection": int,
    "explanation": str,
    "group": str,
    "id": int,
    "startSelection": int,
    "subtype": str,
    "tag": str,
    "type": str,
}

selection_keys_set = set(selection_keys2type.keys())


def is_wrong_types(selection):
    results = {}
    for key, type in selection_keys2type.items():
        if not isinstance(selection[key], type):
            results[key] = str(type)
    return results


def get_store_data(response, file_name):
    store_data = copy.deepcopy(response["rule_based_response_selector"])
    start_data = 0
    end_data = len(response["annotations"]["basic_reader"]["standard_markup"]["text"])
    selections = []
    selections_errors = []
    used_ids = []
    for selection in store_data.get("selections", []):
        start_selection = selection["startSelection"]
        end_selection = selection["endSelection"]
        if start_selection < start_data or end_selection > end_data:
            selection["error_msg"] = "out of essay boundaries"
            selections_errors += [selection]
        elif start_selection == end_selection:
            selection["error_msg"] = "equal start and end"
            selections_errors += [selection]
        elif start_selection > end_selection:
            selection["error_msg"] = "start_selection more then end_selection"
            selections_errors += [selection]
        elif len(set(selection.keys()).intersection(selection_keys_set)) != len(selection_keys_set):
            selection["error_msg"] = f"set of keys has to be equal {selection_keys_set}"
            selections_errors += [selection]
        elif is_wrong_types(selection):
            selection["error_msg"] = f"wrong types {is_wrong_types(selection)}"
            selections_errors += [selection]
        elif selection["id"] in used_ids:
            selection["error_msg"] = f" id {selection['id']} is repeated, used ids = {used_ids}"
            selections_errors += [selection]
        else:
            selections += [selection]
            used_ids += [selection["id"]]
    store_data["selections"] = selections
    return store_data, selections_errors
