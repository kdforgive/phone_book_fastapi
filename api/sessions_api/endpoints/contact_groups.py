from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from db import api_models

router = APIRouter()


@router.get('/contact_groups', status_code=200, tags=['contacts'])
def show_contact_groups(db: Session = Depends(database.get_db)):
    return api_models.ContactGroups.get_list_of_contact_groups(db)
