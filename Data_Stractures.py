"""
This file contains the required classes 
Stack , Queue , HashTable
"""

# LIFO structure - used here for the search history
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        if len(self._items) == 0:
            return True
        return False

    def __str__(self):
        return f"{self._items}"


# FIFO structure - used here for the waiting/processed request queues
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)


# Custom hash table with separate chaining (each bucket is a list)
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = {}
        for i in range(size):
            self.table[i] = []

    # Maps a key to a bucket index
    def hash(self, key):
        return key % self.size

    # Bonus --> Hash Collision Handling
    def get(self, key):
        """
        Handles hash collisions via separate chaining 
        and returns the exact matching record or None
        """
        column = self.hash(key)
        bucket = self.table[column]

        for req in bucket:
            if req.get("Request ID") == key:
                return req
        return None

    # Appends to the bucket instead of overwriting -> collisions are kept, not lost
    def put(self, key, value):
        bucket = self.table[self.hash(key)]
        if value not in bucket:
            bucket.append(value)

    # Flattens every bucket into a single list of records
    def get_all(self):
            all_items = []
            for bucket in self.table.values():
                if bucket is not None:
                    if isinstance(bucket, list):
                        for item in bucket:
                            all_items.append(item)
                    else:
                        all_items.append(bucket)
            return all_items
    
    def __str__(self):
        return str(self.table)
