from fastapi import APIRouter, Request
from .config import global_tree_name
from ..db_manager.db_utils import is_year_in_db, get_larger_tree_size_in_db, select_all_docs_in_year, select_document_with_tree_size, select_document_with_value
from .helper import compare_roots, sanitize_doc, has_missing_request_data

router = APIRouter()


# Hard coded endpoint for tests
@router.get("/all_roots/")
async def no_year():
    return {"message": "No year selected"}


# Get all roots from election in year
@router.get("/all_roots/{year}/")
async def get_documents(year):
    results = select_all_docs_in_year(global_tree_name, year)
    return results


# Get root object with given value
@router.get("/check_root/{year}/{value}")
async def get_documents(year, value):
    results = select_document_with_value(global_tree_name, year, value)
    if not results:
        return {"match": False, "error": "Raiz não encontrada."}
    else:
        return {"match": True, "root": results}


# Compare given root and root in db with same tree_size in given year collection
@router.post("/check_root/")
async def check_root(request: Request):
    item = await request.json()     # get object sent by user
    year = item.get("year")         # get year from user object
    root = item.get("root")         # get root from user object

    # Check if request is missing data, if it is, stop and respond
    is_missing_response = has_missing_request_data(year, root)
    if is_missing_response:
        return is_missing_response

    # If requested 'year' is not in db, stop and return
    if not is_year_in_db(str(year)):
        return {"match": None,
                "year": False,
                "error_key": "year",
                "error": 'Eleição com "year" informado ainda não existe no sistema.'}

    # If requested 'year' is in db, get larger 'tree_size' available in year's db
    largest_tree_size = get_larger_tree_size_in_db(global_tree_name, str(year))

    # If largest tree_size is null, db is empty, stop and return
    if not largest_tree_size:
        return {"match": None,
                "year": False,
                "error_key": "year",
                "error": 'Eleição com "year" informado ainda não possui dados.'}
    # If largest tree_size is smaller than tree_size requested, stop and return
    elif largest_tree_size < root.get('tree_size'):
        return {"match": None,
                "db": False,
                "error_key": "db",
                "error": 'Banco de dados não alcançou a "root" informada, tente novamente mais tarde.'}

    # Else, get document in db with same tree_size given by user
    db_doc = select_document_with_tree_size(global_tree_name, str(year), root.get('tree_size'))

    # Compare roots from user and from db
    response = compare_roots(root, db_doc)

    # Clean root from db to compose response
    response["db_root"] = sanitize_doc(db_doc)

    # If roots didn't match, add hint to response
    if not response.get("match"):
        response["hint"] = "Verifique se o atributo tree_size enviado contém o valor correto."

    # Send response to client
    return response
