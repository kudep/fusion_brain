# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import time

from flask import Flask, jsonify, request

# # for deeppavlov
# from deeppavlov import build_model

TASK = os.getenv("TASK")


def create_c2c_handler():
    import c2c

    def c2c_handler(instance):
        return c2c.j2p(instance)

    return c2c_handler


def create_htr_handler():
    import htr

    def htr_handler(instance):
        return htr.img2text(instance)

    return htr_handler


def create_vqa_handler():
    import vqa

    def vqa_handler(instance):
        return vqa.img_question2answer(*instance)

    return vqa_handler


def create_zsod_handler():
    import zsod

    def zsod_handler(instance):
        return zsod.labeled_img2box(*instance)

    return zsod_handler


tasks = {
    "c2c": {
        "SERVICE_NAME": "c2c",
        "SERVICE_PORT": 8761,
        "HANDLER": create_c2c_handler,
    },
    "htr": {
        "SERVICE_NAME": "htr",
        "SERVICE_PORT": 8762,
        "HANDLER": create_htr_handler,
    },
    "vqa": {
        "SERVICE_NAME": "vqa",
        "SERVICE_PORT": 8763,
        "HANDLER": create_vqa_handler,
    },
    "zsod": {
        "SERVICE_NAME": "zsod",
        "SERVICE_PORT": 8764,
        "HANDLER": create_zsod_handler,
    },
}
SERVICE_NAME = tasks[TASK]["SERVICE_NAME"]
SERVICE_PORT = tasks[TASK]["SERVICE_PORT"]
HANDLER = tasks[TASK]["HANDLER"]()


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/model", methods=["POST"])
def respond():
    st_time = time.time()

    responses = [HANDLER(instance) for instance in request.json]

    total_time = time.time() - st_time
    logger.info(f"{SERVICE_NAME} exec time: {total_time:.3f}s")
    return jsonify(responses)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=SERVICE_PORT)
