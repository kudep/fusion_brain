import logging

from sentence_transformers import SentenceTransformer
from scipy import spatial

from .helpers import log_exceptions

logger = logging.getLogger(__name__)


def cosine(v1, v2):
    return 1 - spatial.distance.cosine(v1, v2)


with log_exceptions(logger):
    logger.info("loading sentence transformer...")
    sentence_transformer = \
        SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
    logger.info("sentence transformer is ready")


def get_similarities(labels, suggestions):
    sentences = labels + suggestions
    logger.info(f"checking for similarities: labels={labels}, suggestions={suggestions}")
    embeddings = sentence_transformer.encode(sentences)
    return [[cosine(label, embedding)
             for embedding in embeddings[len(labels):]]
            for label in embeddings[:len(labels)]]
