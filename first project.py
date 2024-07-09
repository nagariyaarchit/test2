from csv import DictReader
import csv
import json

path = "printing.csv"
file = open(path,"r")
file_type = DictReader(file)
list_of_peoples = list(file_type)
new_list = []
for list_of_people in list_of_peoples:
     x = list_of_people
     new_list.append(x)
     
with open("sample.json", "w") as outfile:
    json.dump(new_list, outfile)
