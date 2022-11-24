import logging.config
import uvicorn
import json


def get_logging_config() -> dict:
    with open('logs/log_config.json', 'r', encoding='UTF-8') as r_file:
        config = json.load(r_file)
    return config


log_config = get_logging_config()
logging.config.dictConfig(log_config)
uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
uvicorn_log_config['formatters']['default']['fmt'] = log_config['formatters']['console_fmt']['format']
uvicorn_log_config['formatters']['access']['fmt'] = log_config['formatters']['console_fmt']['format']
logger = logging.getLogger("uvicorn")
logger.propagate = False
