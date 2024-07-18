class sets():
    def __init__(self):
        self.set = []
        self.not_duplicate_set = []

    def add(self, obj):
        self.set.append(obj)
        self.not_duplicate_set = []
        for i in range(0,len(self.set)):
            current_value = self.set[i]
            for j in range(0,len(self.set)):
                if i != j and current_value == self.set[j]:
                    break
            if current_value not in self.not_duplicate_set:
                self.not_duplicate_set.append(current_value)
        self.set.clear()
        self.set = self.not_duplicate_set
        print(self.set)

    def discard(self, obj):
        self.discard_list = []
        for i in range(0,len(self.set)):
            if self.set[i] == obj:
                index = i
                break
        for j in range(0,len(self.set)):
            if j == index:
                print("removed")
            else:
                self.dicard_list.append(self.set[i])
        self.set.clear()
        self.discard_list = self.set.clear

    def new_list_no_duplicates(self, mylist):
        self.new_list = []
        for i in range(0,len(mylist)):
            current_value = mylist[i]
            for j in range(0,len(mylist)):
                if i != j and current_value == mylist[j]:
                    break
            if current_value not in self.set and current_value not in self.new_list:
                self.new_list.append(current_value)

    def union(self, mylist):
        self.list1 = []
        self.new_list_no_duplicates(mylist)
        for i in range(0,len(self.set)):
            self.list1.append(self.set[i])
        for i in range(0,len(self.new_list)):
            self.list1.append(self.new_list[i])
        print(self.list1)

    def intersection(self,mylist):
        self.duplicate_list = []
        for i in range(0,len(mylist)):
            current_value = mylist[i]
            if current_value in self.set:
                self.duplicate_list.append(current_value)
        print(self.duplicate_list)


        
any_variable = sets()
any_variable.add("apple")
any_variable.add("banana")
any_variable.add("cherry")
any_variable.add("apple")
set2 = [1, 2, 3, "watermelon", 2, "cherry"]
set4 = any_variable.union(set2)
set3 = any_variable.intersection(set2)


