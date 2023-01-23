import csv
import os

path = os.path.join(os.path.dirname(__file__))
with open(f'{path}/list.txt') as file:
    
    reader = csv.reader(file, delimiter=':')
    for line in reader:
        id = line[0]
        name = line[1]
        yamlline = f"- model: mainpage.champion\n  pk: {id}\n  fields:\n    name:{name}\n"
        with open('champions.yaml', "a", encoding="utf-8") as output:
            output.write(yamlline)

            


