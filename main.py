import csv_to_json
import database_driver as driver
import Region as reg


csv_file_path = r'Dataset/130142-21data043021.csv'
json_file_path = r'Dataset/130142-21data043021.json'

csv_to_json.convert_to_json(csv_file_path,json_file_path)


# Pymongo
#driver.clear_collection()
#driver.insert_json_file(json_file_path)




# mongoengine
reg.insert_population_csv(csv_file_path,'utf8')








