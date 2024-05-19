from fastapi import APIRouter
from .config import global_tree_name
from ..db_manager.db_utils import get_db_collection

router = APIRouter()


# Hard coded endpoint for tests
@router.get("/all_roots/")
async def no_year():
    return {"message": "No year selected"}


# Get all roots from election in year
@router.get("/all_roots/{year}/")
async def get_documents(year):
    collection = get_db_collection(year, global_tree_name)
    documents = collection.find({})
    results = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    return results
