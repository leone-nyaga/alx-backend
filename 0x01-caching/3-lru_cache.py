from base_caching import BaseCaching

class LRUCache(BaseCaching):
    """ LRU caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.cache_data = {}
        self.cache_order = []  # List to maintain the order of keys

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the item and move it to the end to mark it as recently used
            self.cache_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Cache is full, remove the least recently used item (LRU)
            lru_key = self.cache_order.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD: {}".format(lru_key))

        # Add the item to the cache and update the order list
        self.cache_data[key] = item
        self.cache_order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        # Move the accessed item to the end to mark it as recently used
        self.cache_order.remove(key)
        self.cache_order.append(key)
        return self.cache_data[key]
