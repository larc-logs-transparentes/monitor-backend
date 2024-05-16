# Log Server data fetcher constants:
global_tree_name = "global_tree"
election_name = "election_545"
election_year = "2023"

url = "http://localhost:8080"

tree_info_api = "/tree?tree_name="
tree_root_api = "/tree/tree-root?tree_name="
tree_all_roots_api = "/tree/all-roots-global-tree"
tree_all_roots_api_since = "/tree/all-roots-global-tree?initial_root_value="

url_get_global_tree_length = f"{url}{tree_info_api}{global_tree_name}"
url_get_global_tree_last_root = f"{url}{tree_root_api}{global_tree_name}"
url_get_global_tree_all_roots = f"{url}{tree_all_roots_api}"
url_get_global_tree_all_roots_since = f"{url}{tree_all_roots_api_since}"
