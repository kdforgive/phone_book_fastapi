from fastapi import APIRouter, Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from db import database
from db import api_models
from core import schemas
from core.endpoint_checks import EndpointFieldValidation
from core.endpoint_checks import EndpointSessionValidation
from typing import Optional
import logging
from core.hashing import Hash

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put('/change_field', status_code=200, tags=['contacts'])
@EndpointSessionValidation.user_id_validation
def change_field(field: schemas.ChangeFields, session_token: Optional[str] = Cookie(None),
                 db: Session = Depends(database.get_db)) -> None:

    allowed_groups = EndpointFieldValidation.allowed_groups(db)
    if field.field_name_to_change == 'email' and not EndpointFieldValidation.email_check(field.field_value_to_change):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')
    if field.field_name_to_change == 'group_name' and field.field_value_to_change not in allowed_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='group doesn\'t exist')

    # read search_hashed_id from Contacts table
    decoded_contact_id = Hash.decoded_id(field.field_id)
    api_models.Contacts.update_contact(decoded_contact_id, field.field_name_to_change, field.field_value_to_change, db)
