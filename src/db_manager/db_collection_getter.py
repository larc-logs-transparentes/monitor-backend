from .db_connection import get_db_client


# From database election, select Collection with name
def get_db_collection(name):
    client = get_db_client()
    db = client["elections"]
    collection = db[name]
    return collection
