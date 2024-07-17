import random
class array_list():
    def __init__(self):
        self.length = 10
        self.list = [None] * 10
        self.currentSize = 0

    def new_array(self):
        self.length *= 2
        self.new = [None] * self.length
        for i in range(0,len(self.list)):
            self.new[i] = self.list[i]
        self.list.clear()
        self.list = self.new

    def append(self, obj):
        if (len(self.list)-1) == self.currentSize:
            ary.new_array() 
        else:
            self.list[self.currentSize] = obj
            self.currentSize += 1
        return self.list

        

ary = array_list()
ary.append("hello")
print(ary.append("obj"))
for i in range(0,50):
    ary.append(i)
print(ary.append("g"))




