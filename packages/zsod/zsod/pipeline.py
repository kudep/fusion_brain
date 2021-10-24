# import logging
from collections import defaultdict
from copy import deepcopy

import numpy as np
import torch
from PIL.Image import Image

from .helpers import pil_to_cv2
from .region_proposal import predict_regions, filter_regions
from .classifier import get_categories_probs, get_cat_synset
from .similarity_check import get_similarities
from .translate import has_cyrillic, translate_ru_en

# logger = logging.getLogger(__name__)


def translate_labels(labels):
    ru_labels = [label for label in labels if has_cyrillic(label)]
    ru_inds = [i for i, label in enumerate(labels) if has_cyrillic(label)]

    en_labels = deepcopy(labels)

    if ru_labels:
        translated_labels = translate_ru_en(ru_labels)
        # logger.info(f"russian labels were translated: {translated_labels}")

        for ind, en_label in zip(ru_inds, translated_labels):
            en_labels[ind] = en_label

    return en_labels


def search_on_image(image: Image,
                    labels,
                    classification_threshold=0.2,
                    similarity_threshold=0.3,
                    overlap_threshold=0.5,
                    same_class_overlap_threshold=0.3,
                    n_predictions_for_region=3):
    en_labels = translate_labels(labels)

    regions = predict_regions(pil_to_cv2(image))
    regions = filter_regions(regions, threshold=overlap_threshold)

    detections = []
    for region in regions:
        # logger.info(f"analysing region: {region.unwrap()}")
        cropped = image.crop(box=region.unwrap())
        probs = get_categories_probs(cropped)

        topn_prob, topn_catid = torch.topk(probs, n_predictions_for_region)
        filt = topn_prob > classification_threshold
        if not filt.any():
            # logger.info("no matches, skipping region")
            continue
        topn_prob = topn_prob[filt]
        topn_catid = topn_catid[filt]
        # logger.info("got top:")
        # for i, (prob, idx) in enumerate(zip(topn_prob, topn_catid)):
        #     logger.info(f"{i}: {get_cat_synset(idx)[0]} {prob}")
        similarities = get_similarities(en_labels,
                                        [', '.join(get_cat_synset(idx))
                                         for idx in topn_catid])
        # logger.info(f"similarities: {similarities}")
        best_match = np.array(similarities).argmax()
        best_match_classifier = best_match % len(topn_prob)
        best_match_label = best_match // len(topn_prob)
        if topn_prob[best_match_classifier] > classification_threshold and \
                similarities[best_match_label][
                    best_match_classifier] > similarity_threshold:
            region.probability = topn_prob[best_match_classifier]
            region.idx = topn_catid[best_match_classifier]
            region.label = labels[best_match_label]
            # logger.info(
            #     f"approved best match: {get_cat_synset(region.idx)[0]} " +
            #     f"as label {en_labels[best_match_label]}")
            detections.append(region)

    # remove everything that overlaps significantly
    # among detections of the same class
    detections_by_category = defaultdict(list)
    for detection in detections:
        detections_by_category[detection.label].append(detection)
    detections = []
    for cat, cat_detections in detections_by_category.items():
        detections += filter_regions(cat_detections,
                                     threshold=same_class_overlap_threshold)
    return detections
