import uvicorn
from fastapi import FastAPI
from db.database import engine
from api.mock.api import api_router
from api.mock import api_models

api_models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

app.include_router(api_router, prefix='/v1')


# def main():
#     """Run app"""
#     uvicorn.run('settings.main:app', host='localhost', port=6969, reload=True)
#
#
# if __name__ == '__main__':
#     main()
#
