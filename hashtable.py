class HashTable:
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self,key):
        return hash(key) % self.capacity

    # Insertting a new item into the hash table
    def insert(self, key, item):
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = item
                return

        bucket.append([key, item])
        self.size += 1

        # Checking to see if the table needs to be resized
        if self.size / self.capacity > 0.7:
            self.resize()

    # Resizing the hash table
    def resize(self):
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for key, item in bucket:
                self.insert(key, item)

    def lookup(self, key):
        bucket = self.table[self._hash(key)]
        for k, package in bucket:
            if k == key:
                return package
        return None