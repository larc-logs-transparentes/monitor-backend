def compare_roots(user_root, db_root):
    response = {
        "signature": user_root.get("signature") == db_root.get("signature"),
        "value": user_root.get("value") == db_root.get("value")
    }
    response["match"] = response.get("signature") and response.get("value")
    return response
