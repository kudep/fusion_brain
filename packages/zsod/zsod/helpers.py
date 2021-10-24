from contextlib import contextmanager

import numpy as np
from PIL.Image import Image


def pil_to_cv2(image: Image):
    return np.array(image.convert('RGB'))[:, :, ::-1]


@contextmanager
def log_exceptions(logger):
    try:
        yield None
    except Exception as e:
        logger.exception(e)
        raise e
