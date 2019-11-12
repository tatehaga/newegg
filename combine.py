#!/usr/bin/python3
import json

with open('data2.json') as json_file:
    graphics = json.load(json_file)
with open('data_cases.json') as json_file2:
    cases = json.load(json_file2)

data = {}
data.update(graphics)
data.update(cases)


with open('cases_graphics_data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)