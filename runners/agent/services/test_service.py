# flake8: noqa
#
##########################################################################
# Attention, this file cannot be changed, if you change it I will find you#
##########################################################################
#
import os
import time
import difflib

import requests

TASK = os.getenv("TASK")


tasks = {
    "c2c": {
        "SERVICE_NAME": "c2c",
        "SERVICE_PORT": 8761,
        "REQUESTS": [
            'class HelloWorld {public static void main(String[] args) {System.out.println("Hello, world.");}}'
        ],
        "RESPONSES": [
            '#!/usr/bin/env python\n""" generated source for module 27a14ee2-0d0b-4aec-9358-8558ce5faed7 """\nclass HelloWorld(object):\n    """ generated source for class HelloWorld """\n    @classmethod\n    def main(cls, args):\n        """ generated source for method main """\n        print("Hello, world.")\n\n'
        ],
        "COMP": lambda x, y: difflib.SequenceMatcher(None, x.split(), y.split()).ratio() < 0.9,
    },
    "htr": {
        "SERVICE_NAME": "htr",
        "SERVICE_PORT": 8762,
        "REQUESTS": ["/htr_data/data/img.png"],
        "RESPONSES": ["последовал"],
        "COMP": lambda x, y: x != y,
    },
    "vqa": {
        "SERVICE_NAME": "vqa",
        "SERVICE_PORT": 8763,
        "REQUESTS": [("/vqa_data/data/dog.jpg", "Кто на траве?"), ("/vqa_data/data/dog.jpg", "Who is on the grass?")],
        "RESPONSES": ["Никто", "nobody"],
        "COMP": lambda x, y: x != y,
    },
    "zsod": {
        "SERVICE_NAME": "zsod",
        "SERVICE_PORT": 8764,
        "REQUESTS": [("/zsod_data/data/dog.jpg", "Собака")],
        "RESPONSES": [[[36.53443145751953, 0.0, 989.3976974487305, 1038.1778564453125]]],
        "COMP": lambda x, y: x != y,
    },
}
SERVICE_NAME = tasks[TASK]["SERVICE_NAME"]
SERVICE_PORT = tasks[TASK]["SERVICE_PORT"]
REQUESTS = tasks[TASK]["REQUESTS"]
RESPONSES = tasks[TASK]["RESPONSES"]
COMP = tasks[TASK]["COMP"]


def test_skill():
    url = f"http://0.0.0.0:{SERVICE_PORT}/model"
    warnings = 0

    for request, true_response in zip(REQUESTS, RESPONSES):
        st_time = time.time()
        response = requests.post(url, json=[request], timeout=180).json()[0]
        total_time = time.time() - st_time
        print(f"exec time: {total_time:.3f}s")
        if COMP(response, true_response):
            print("----------------------------------------")
            print(f"unmatch request = {request}")
            print(f"{response} != {true_response}")
            warnings += 1
    assert warnings == 0
    print("SUCCESS!")


if __name__ == "__main__":
    test_skill()
