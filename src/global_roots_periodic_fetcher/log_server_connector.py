import requests

from .config import url, tree_names_api, tree_root_api


# Connects to Log Server endpoint and get all tree names from server
def get_trees_names():
    try:
        response = requests.get(f"{url}{tree_names_api}")
        trees = response.json().get('trees')
        return trees
    except requests.exceptions.RequestException as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(e)


# Connects to Log Server endpoints and gets last entry for each tree
def get_last_entry_of_trees(tree_names):
    last_entries = {}
    for tree_name in tree_names[1:]:
        try:
            # TODO: check if this endpoint is still up
            response = requests.get(f"{url}{tree_names_api}{tree_name}")
            trees = response
            return trees
        except requests.exceptions.RequestException as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError(e)
