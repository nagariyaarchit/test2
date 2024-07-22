class HashMaps:
    def __init__(self):
        self.size = 10
        self.arr = [[] for i in range(0,self.size)]
    
    def get_hash(self, key):
        h = 0
        for char in key:
            h += ord(char)
        return h % self.size
    
    def __getitem__(self,key):
        h = self.get_hash(key)
        for element in self.arr[h]:
            if element[0] == key:
                print(element[1])

    def __setitem__(self, key, Val):
        h = self.get_hash(key)
        found = False
        for idx, element in enumerate(self.arr[h]):
            if len(element)==2 and element[0] == key:
                self.arr[h][idx] = (key,Val)
                found = True
                break
        if not found:
            self.arr[h].append((key,Val))

    def __delitem__(self,key):
         h = self.get_hash(key)
         for index, element in enumerate(self.arr[h]):
             if element[0] == key:
                del self.arr[h][index]

t = HashMaps()
t["march 6"] = 128
t["march 6"] = 78
t["march 9"] =67
t["march 8"] = 4
t["march 17"] = 459
print(t.arr)
del t["march 8 "]
print(t.arr)