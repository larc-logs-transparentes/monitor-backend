from fastapi import APIRouter

router = APIRouter()


@router.get("/roots/", tags=["roots"])
async def read_users():
    return [{"root": "my_root_1"}, {"root": "my_root_2"}]
