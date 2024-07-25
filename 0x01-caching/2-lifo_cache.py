#!/usr/bin/python3

from base_caching import BaseCaching

class LIFOCache(BaseCaching):
    """ LIFO caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.cache_order = []  # List to maintain the order of keys

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the item if it already exists
            self.cache_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Cache is full, remove the last item added (LIFO)
            last_key = self.cache_order.pop()
            del self.cache_data[last_key]
            print("DISCARD: {}".format(last_key))

        # Add the item to the cache and update the order list
        self.cache_data[key] = item
        self.cache_order.append(key)

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
