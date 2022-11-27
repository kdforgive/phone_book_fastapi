from fastapi import APIRouter

router = APIRouter()


@router.post('/create_contact')
def create_contact():
    """
    1: groups in dict or separate sql table, check only allowed group
    """
    pass
