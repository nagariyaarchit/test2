class HashMaps:
    def __init__(self):
        self.size = 10
        self.map = [[] for i in range(0,self.size)]
        # print(self.map)

    def hashing_function(self, key):
        hashed_key =  hash(key) % self.size
        return hashed_key

    def set(self, key, value):
        hash_key = self.hashing_function(key)
        key_exists = False
        slot = self.map[hash_key]
        for i, kv in range(0,len(slot)):
            k, v = kv
            if key == k:
                key_exists = True 
        if key_exists:
            slot[i] = ((key,value))
        else:
            slot.append((key,value))

    def get(self, key):
        hash_key = self.hashing_function(key)
        slot = self.map[hash_key]
        for kv in slot:
            k, v = kv
            if key == k:
                return v
            else:
                print("key does not exist")

h = HashMaps()
h.set("Ontario", "Toronto")
h.set("Britishcolumbia", "Vancouver")
h.set("Quebec", "Montreal")

print(h.map)

