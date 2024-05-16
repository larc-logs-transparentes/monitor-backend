from .db_connection import get_db_client


# From database election, select Collection with name
def get_db_collection(db_name, collection_name):
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]
    return collection


def insert_roots_to_collection(collection_name, db_name, roots):
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(roots)
    return result


def select_document_larger_tree_size(collection_name, db_name):
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]
    pipeline = [
        {"$sort": {"tree_size": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    if len(result) > 0:
        return result[0]
    else:
        return {}
