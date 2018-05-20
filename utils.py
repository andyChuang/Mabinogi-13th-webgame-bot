# coding=UTF-8
import json


def load_json(path):
    with open(path) as f:
        content = json.load(f)

    return content