import math
class calculator:
    def __init__(self,num1,num2):
        self.num1 = int(num1)
        self.num2 = int(num2)
    def add(self):
        self.sum = self.num1 + self.num2
        return self.sum
    def subtract(self):
        self.sum2 = self.num1 - self.num2
        return self.sum2
    def multiply(self):
        self.multiply = self.num1*self.num2
        return self.multiply
    def divide(self):
        greatest_denom = math.gcd(self.num1,self.num2)
        self.reduced_num1 = self.num1//greatest_denom
        self.reduced_num2 = self.num2//greatest_denom
        self.fraction = str(self.reduced_num1) + "/" + str(self.reduced_num2)
        return self.fraction


num1 = int(input("Enter the first integer:"))
num2 = int(input("Enter the second integer:"))
sets = calculator(num1, num2)    
choice = int(input("select 1 to add, select 2 for subtraction, select 3 for multiplication, select 4 for division:"))
if choice == 1:
    print(sets.add())
if choice == 2:
    print(sets.subtract())
if choice == 3:
    print(sets.multiply())
if choice == 4:
    print(sets.divide())