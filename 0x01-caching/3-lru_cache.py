#!/usr/bin/env python3
"""LRU Caching"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ Defines a LRU cache system """

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
                self.keys.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last = self.keys.pop(0)
                print("DISCARD: {}".format(last))
                del self.cache_data[last]
            self.keys.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Return the value linked to key in self.cache_data.
        Return None if key is None or doesn't exist
        """
        if key in self.cache_data:
            self.keys.remove(key)
            self.keys.append(key)
        return self.cache_data.get(key, None)
