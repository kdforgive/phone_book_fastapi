from fastapi import APIRouter
from api.sessions_api.endpoints.login import router as login_router
from api.sessions_api.endpoints.user import router as user_router
from api.sessions_api.endpoints.contact_groups import router as show_contact_groups_router
from api.sessions_api.endpoints.create_contact import router as create_contact
from api.sessions_api.endpoints.contacts import router as search_in_my_contacts
from api.sessions_api.endpoints.change_field import router as change_contact
from api.sessions_api.endpoints.delete_contact import router as delete_contact

api_router = APIRouter()

api_router.include_router(login_router)
api_router.include_router(user_router)
api_router.include_router(show_contact_groups_router)
api_router.include_router(create_contact)
api_router.include_router(search_in_my_contacts)
api_router.include_router(change_contact)
api_router.include_router(delete_contact)
