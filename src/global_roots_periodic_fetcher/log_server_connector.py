import requests

from .config import url_get_global_tree_length, url_get_global_tree_last_root, url_get_global_tree_all_roots, url_get_global_tree_all_roots_since


# Connects to Log Server endpoint to get global tree length
def get_global_tree_length():
    try:
        response = requests.get(url_get_global_tree_length)
        length = response.json().get('length')
        return length
    except requests.exceptions.RequestException as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)


# Connects to Log Server endpoint to get last hash root from global tree
def get_global_tree_last_root():
    try:
        response = requests.get(url_get_global_tree_last_root)
        root = response.json().get('value')
        return root
    except requests.exceptions.RequestException as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)


# Connects to Log Server endpoint and get all tree roots from server
def get_global_tree_all_roots():
    try:
        response = requests.get(url_get_global_tree_all_roots)
        roots = response.json().get('roots')
        return roots
    except requests.exceptions.RequestException as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)


# Connects to Log Server endpoint and get younger tree roots than given root since  from server
def get_global_tree_all_roots_since(last_root):
    try:
        url = url_get_global_tree_all_roots_since + last_root
        response = requests.get(url)
        roots = response.json().get('roots')
        return roots
    except requests.exceptions.RequestException as e:
        print("exception:", e)
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)

