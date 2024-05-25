from fastapi import APIRouter, Request
from .config import global_tree_name
from ..db_manager.db_utils import select_all_docs_in_year, select_document_larger_tree_size, select_document_with_tree_size, select_document_with_value
from .helper import compare_roots

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
    if root:                        # get tree_size from user object if there is a root object
        tree_size = root.get("tree_size")
    else:
        tree_size = None

    # Get the maximum tree_size from the global_tree of given year
    db_doc_max_tree_size = select_document_larger_tree_size(global_tree_name, str(year))
    # Get document in db with same tree_size given by user
    db_doc = select_document_with_tree_size(global_tree_name, str(year), tree_size)

    # Check for absence of properties and respond accordingly
    if root is None:
        return {"match": False,
                "root": None,
                "error_key": "root",
                "error": "Objeto root ausente na requisição."}

    elif tree_size is None:
        return {"match": False,
                "tree_size": None,
                "error_key": "tree_size",
                "error": "Atributo tree_size ausente no objeto root."}

    elif year is None:
        return {"match": False,
                "year": None,
                "error_key": "year",
                "error": "Atributo year ausente na requisição."}

    elif db_doc_max_tree_size == {}:
        return {"match": False,
                "db": None,
                "error_key": "db",
                "error": "Banco de dados ainda não populado, tente novamente mais tarde."}

    elif tree_size > db_doc_max_tree_size.get("tree_size"):
        return {"match": False,
                "db": False,
                "error_key": "db",
                "error": "Banco de dados ainda não alcançou a raíz pedida, tente novamente mais tarde."}

    # if every property is present, compare given root object with object retrieved from database
    elif db_doc_max_tree_size.get("tree_size") >= tree_size >= 0:
        response = compare_roots(root, db_doc)
        response["db_root"] = db_doc
        if not response.get("match"):
            response["hint"] = "Verifique se o atributo tree_size enviado contém o valor correto."
        return response

    else:   # General error
        return {"match": False, "error_key": None, "error": "Erro desconhecido"}
