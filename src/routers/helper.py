def compare_roots(user_root, db_root):
    # insert True of False for matching values of 'value' and 'signature'
    response = {
        "value": user_root.get('value') == db_root.get('value'),
        "signature": user_root.get('signature') == db_root.get('signature')
    }
    
    # insert True for 'match' if both 'value' and 'signature' are True, otherwise insert False
    response["match"] = response.get('signature') and response.get('value')

    # if any value is False, set 'error_key
    if not response.get('value'):
        response["error_key"] = "value"
    elif not response.get('signature'):
        response["error_key"] = "signature"

    return response


# Remove unnecessary data from response
def sanitize_doc(doc):
    doc.pop('_id', None)
    doc.pop('timestamp', None)
    doc.pop('tree_name', None)
    return doc
