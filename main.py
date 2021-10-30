import csv_to_json
import database_driver as driver


csv_file_path = r'data/export-sluzby-2021-10.csv'
json_file_path = r'data/export-sluzby-2021-10.json'

csv_to_json.convert_to_json(csv_file_path,json_file_path)

driver.clear_collection()
driver.insert_json_file(json_file_path)






