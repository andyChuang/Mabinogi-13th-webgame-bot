# coding=UTF-8
import json


def load_account(config_path):
    with open(config_path) as f:
        content = json.load(f)

    return content