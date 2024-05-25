from .db_connection import get_db_client


# From database election, select Collection with name
def get_db_collection(db_name, collection_name):
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]
    return collection


def select_all_docs_in_year(collection_name, db_name):
    collection = get_db_collection(db_name, collection_name)
    documents = collection.find({})
    results = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    return results


def insert_roots_to_collection(collection_name, db_name, roots):
    collection = get_db_collection(db_name, collection_name)
    result = collection.insert_many(roots)
    return result


# Select from given db collection the document in which property "tree_size" is bigger
def select_document_larger_tree_size(collection_name, db_name):
    collection = get_db_collection(db_name, collection_name)
    pipeline = [
        {"$sort": {"tree_size": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    if len(result) > 0:
        return result[0]
    else:
        return {}


def select_document_with_tree_size(collection_name, db_name, tree_size):
    collection = get_db_collection(db_name, collection_name)
    documents = collection.find({"tree_size": tree_size})
    result = stringify_docs_ids(documents)
    if len(result) > 0:
        return result[0]
    else:
        return {}


# Select document from db with given root value
def select_document_with_value(collection_name, db_name, value):
    collection = get_db_collection(db_name, collection_name)
    documents = collection.find({"value": value})
    result = stringify_docs_ids(documents)
    if len(result) > 0:
        return result[0]
    else:
        return {}


# Transform Mongo ID object to string
def stringify_docs_ids(documents):
    results = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        results.append(doc)
    return results
