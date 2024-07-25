#!/usr/bin/env python3
"""LFU Caching"""

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """Defines a LFU cache system"""

    def __init__(self):
        """Initializes the cache and
        frequency tracking
        """
        super().__init__()
        self.usage = {}
        self.keys = []

    def put(self, key, item):
        """
        Add an item to the cache with
        LFU eviction policy and LRU tiebreaker
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.usage[key] += 1
                self.keys.remove(key)
                self.keys.append(key)
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    # Get the least used item
                    lfu_key = min(self.usage, key=self.usage.get)
                    if lfu_key in self.cache_data:
                        del self.cache_data[lfu_key]
                        del self.usage[lfu_key]
                        del self.keys[self.keys.index(lfu_key)]
                        print("DISCARD:", lfu_key)
                self.cache_data[key] = item
                self.usage[key] = 1
                self.keys.append(key)

    def get(self, key):
        """
        Retrieve an item from the cache
        """
        if key in self.cache_data:
            self.usage[key] += 1
            self.keys.remove(key)
            self.keys.append(key)
            return self.cache_data[key]
        return None
