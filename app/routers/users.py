from fastapi import APIRouter
""" from app.services.user_service import get_users """
from app.services.user_service import get_users

router = APIRouter(prefix="/users")

@router.get("/")
def list_users():
    return get_users()