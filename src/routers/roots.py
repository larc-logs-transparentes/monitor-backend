from fastapi import APIRouter
from ..db_manager.db_collection_getter import get_db_collection

router = APIRouter()


# Hard coded endpoint for tests
@router.get("/all_roots/")
async def no_year():
    return {"message": "No year selected"}


# Get all roots from election in year
@router.get("/all_roots/{year}")
async def get_documents(year):
    collection = get_db_collection(year)
    documents = collection.find({})
    results = []
    for doc in documents:
        results.append(doc.get('root'))
    return results
