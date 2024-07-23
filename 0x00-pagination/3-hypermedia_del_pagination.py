#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves a subset of data from the dataset
        based on the given index and page size.

        Args:
            index (int, optional): The starting index of
            the subset. Defaults to None.
            page_size (int, optional): The number of items to
            include in the subset. Defaults to 10.

        Returns:
            dict: A dictionary containing the following information:
                - index (int): The starting index of the subset.
                - data (list): The subset of data.
                - page_size (int): The number of items in the subset.
                - next_index (int): The index of the next subset.

        Raises:
            AssertionError: If the index is negative or out of range.

        """
        assert index is None or index >= 0, "Invalid index value"

        dataset = self.dataset()
        dataset_length = len(dataset)

        if index is None:
            index = 0
        else:
            assert index < dataset_length, "Index out of range"

        next_index = min(index + page_size, dataset_length)
        data = dataset[index:next_index]

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index
        }
