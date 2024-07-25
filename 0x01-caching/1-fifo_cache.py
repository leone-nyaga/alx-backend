#!/usr/bin/env python3
"""FIFO caching"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ Defines a FIFO cache system """

    def __init__(self):
        """ Initializes the cache """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        Assign item value for the key in
        self.cache_data
        if neither key nor item is None
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                first = self.keys.pop(0)
                print("DISCARD: {}".format(first))
                del self.cache_data[first]
            self.keys.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Return the value linked to key in self.cache_data.
        Return None if key is None or doesn't exist
        """
        return self.cache_data.get(key, None)
