#!/usr/bin/python3


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.cache_order = []  # List to maintain the order of keys

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Cache is full, remove the first item added (FIFO)
            first_key = self.cache_order.pop(0)
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))

        # Add the item to the cache and update the order list
        self.cache_data[key] = item
        if key not in self.cache_order:
            self.cache_order.append(key)

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
