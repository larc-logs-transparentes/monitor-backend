def compare_roots(user_root, db_root):
    # insert True of False for matching values of 'value' and 'signature'
    response = {
        "match_details": {
            "value": user_root.get('value') == db_root.get('value'),
            "signature": user_root.get('signature') == db_root.get('signature')
        }
    }
    
    # insert True for 'match' if both 'value' and 'signature' are True, otherwise insert False
    response["match"] = response.get('match_details').get('signature') and response.get('match_details').get('value')

    return response


# Remove unnecessary data from response
def sanitize_doc(doc):
    doc.pop('_id', None)
    doc.pop('timestamp', None)
    doc.pop('tree_name', None)
    return doc


def has_missing_request_data(year, root):
    # If field "year" is not present, stop and return
    if not year:
        return {"match": None,
                "error": "Missing parameter",
                "message": "Atributo \"year\" ausente na requisição."}

    # If field "root" is not present, stop and return
    if not root:
        return {"match": None,
                "error": "Missing parameter",
                "message": "Atributo \"root\" ausente na requisição"}
    # If field "root" is present, check in it for presence of 'value', 'tree_size' and 'signature'
    else:
        if not root.get('value'):
            return {"match": None,
                    "error": "Missing parameter",
                    "message": 'Atributo "value" ausente em "root".'}
        if not root.get('tree_size'):
            return {"match": None,
                    "error": "Missing parameter",
                    "message": 'Atributo "tree_size" ausente em "root".'}
        if not root.get('signature'):
            return {"match": None,
                    "error": "Missing parameter",
                    "message": 'Atributo "signature" ausente em "root".'}

    return False
