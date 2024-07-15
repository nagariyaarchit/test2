import array

class temperature:
    def __init__(self,array):
        self.array = array
    def convert_to_celsius(self):
        self.celcius_temperature = []
        for degree in self.array:
            self.celcius = (degree - 32) * (5/9)
            self.celcius_temperature.append(self.celcius)
        return self.celcius_temperature
    def statistics(self):
        self.total = 0
        self.biggest_temp = 0
        self.smallest_temp = self.celcius_temperature[0]
        for degree in self.celcius_temperature:
            self.total += degree
            if degree >= self.biggest_temp:
                self.biggest_temp = degree
            if self.smallest_temp >= degree:
                self.smallest_temp = degree
        average_temperature = self.total/len(self.celcius_temperature)
        return average_temperature, self.biggest_temp, self.smallest_temp


farhennite = array.array("i",[68, 86, 122, 23 , 59, 104])
x = temperature(farhennite)
print(x.convert_to_celsius())
print(x.statistics())