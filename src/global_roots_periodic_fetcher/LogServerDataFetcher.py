import asyncio
import time

from .log_server_connector import *


class LogServerDataFetcher:
    # Flag to turn on or off the Log Server Data Fetcher
    turn_fetcher_on = True

    # Flag setter
    @classmethod
    def set_turn_fetcher_on(cls, value):
        cls.turn_fetcher_on = value

    # Async method to get data from multiple Log Server endpoints and decide if should copy data or not
    @staticmethod
    async def get_new_data_from_log_server():
        print('get new data')
        count = 0
        while LogServerDataFetcher.turn_fetcher_on:
            try:
                tree_names = get_trees_names()
                last_entries = get_last_entry_of_trees(tree_names)
                print(last_entries)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            await asyncio.sleep(5)  # Sleep for 60 seconds
            if count > 8:
                break
            count += 1

    # Helper method to run async methods in parallel thread
    @staticmethod
    def start_get_data_from_log_server():
        asyncio.run(LogServerDataFetcher.get_new_data_from_log_server())

