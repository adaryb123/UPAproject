import csv
import json
import os

def remove_json_file_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

def convert_to_json(csv_file_path, json_file_path):
    data = {}
    with open(csv_file_path, encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        i = 0
        for row in csv_reader:
            data[i] = row
            i += 1

    remove_json_file_if_exists(json_file_path)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data, indent=4))