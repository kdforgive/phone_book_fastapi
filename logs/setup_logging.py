import json
import logging.config


def read_log_config():
    with open('logs/log_config.json', 'r', encoding='UTF-8') as r_file:
        config = json.load(r_file)
    return logging.config.dictConfig(config)
