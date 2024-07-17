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

    def remove(self, obj):
        for i in range(0,len(self.list)-1):
            if (self.list[i]) == obj:
                self.index = i
                self.new_list = []
                for i in range(0,len(self.list)):
                    if self.index == i:
                        print("pass")
                    else:
                        self.new_list.append(self.list[i])
                self.list.clear()
                self.list = self.new_list
        return self.list

    def reverse(self):
        self.new_list_r = []
        self.list_length = len(self.list) - 1
        for i in range(0,len(self.list)):
            self.new_list_r.append(self.list[self.list_length])
            self.list_length -= 1
        self.list.clear()
        self.list = self.new_list_r

        return self.list

    def pop(self, index):
        self.new_list_p = []
        for i in range(0,len(self.list)-1):
            if index == i:
                print("do nothing")
            else:
                self.new_list_p.append(self.list[i])
        self.list.clear()
        self.list = self.new_list_p
        return self.list


ary = array_list()
ary.append("hello")
print(ary.append("obj"))
for i in range(0,50):
    ary.append(i)
print(ary.remove(34))#cannont remove none
print(ary.pop(3))
print(ary.reverse())



