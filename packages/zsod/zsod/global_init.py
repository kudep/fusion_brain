import os
import logging

import torch

from .helpers import log_exceptions


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

logger = logging.getLogger(__name__)

with log_exceptions(logger):
    cuda = torch.cuda.is_available()
    if cuda:
        torch.cuda.set_device(0)  # singe gpu
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    logger.info(f"zero-shot object detection is set to run on {device}")
