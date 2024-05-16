import asyncio

from src.db_manager.db_utils import *
from .log_server_connector import *
from .config import election_name, election_year


class LogServerDataManager:
    # Flag to turn on or off the Log Server Data Fetcher
    turn_fetcher_on = True

    # Cache of last length and root gotten from server
    last_root_cache = None

    # Flag setter
    @classmethod
    def set_turn_fetcher_on(cls, value):
        cls.turn_fetcher_on = value

    # Async method to get data from multiple Log Server endpoints and decide if should copy data or not
    @classmethod
    async def save_new_data_from_log_server(cls):
        while LogServerDataManager.turn_fetcher_on:
            try:
                if cls.last_root_cache: # if there is cache, get from log server starting at it
                    roots = get_global_tree_all_roots_since(cls.last_root_cache)
                    cls.insert_roots_to_db_collection(False, roots)
                else:   # if there is no cache, check last root in db
                    document = select_document_larger_tree_size(election_name, election_year)
                    last_root_db = document.get("value")
                    if last_root_db:    # if db has roots, get last and get from log server starting at it
                        roots = get_global_tree_all_roots_since(last_root_db)
                        cls.insert_roots_to_db_collection(False, roots)
                    else:   # if db has no roots, get all roots from log server
                        roots = get_global_tree_all_roots()
                        cls.insert_roots_to_db_collection(True, roots)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            await asyncio.sleep(60)  # Sleep for 60 seconds\

    # Helper method to run async methods in parallel thread
    @staticmethod
    def start_get_data_from_log_server():
        asyncio.run(LogServerDataManager.save_new_data_from_log_server())

    # Helper method that inserts roots to db
    @classmethod
    def insert_roots_to_db_collection(cls, is_db_empty, roots):
        if not is_db_empty:
            roots.pop(0)

        if len(roots) > 0:
            result = insert_roots_to_collection(election_name, election_year, roots)
            if result.acknowledged:
                cls.last_root_cache = roots[-1].get('value')
