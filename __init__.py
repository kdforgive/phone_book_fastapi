# import logging.config
# import uvicorn
# from logs.setup_logging import config_logging
#
# log_config = config_logging()
# logging.config.dictConfig(log_config)
# print(type(log_config),'============================================')
# uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
# uvicorn_log_config['formatters']['default']['fmt'] = log_config['formatters']['main_fmt']['format']
# uvicorn_log_config['formatters']['access']['fmt'] = log_config['formatters']['main_fmt']['format']
# logger = logging.getLogger("uvicorn")
# logger.propagate = False
print('abcd----------------------------------------------')