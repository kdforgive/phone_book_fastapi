# from logs import logging_config
from fastapi import FastAPI
from db.database import engine
from api.sessions_api.api import api_router as main_page_router
from db import api_models
import logging

logger = logging.getLogger(__name__)
logger.info('server starting')

api_models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

app.include_router(main_page_router, prefix='/v1')


# def main():
#     """Run app"""
#     uvicorn.run('main:app', host='localhost', port=6969, reload=True)
#
#
# if __name__ == '__main__':
#     main()
